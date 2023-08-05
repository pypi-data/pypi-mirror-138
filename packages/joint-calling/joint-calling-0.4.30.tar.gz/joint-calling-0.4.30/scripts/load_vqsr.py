#!/usr/bin/env python

"""
Imports AS-VQSR site VCF into a HT
"""

import logging
from typing import Optional

import click
import hail as hl

from gnomad.utils.sparse_mt import split_info_annotation

from joint_calling import utils, _version

logger = logging.getLogger('import_vqsr')
logger.setLevel(logging.INFO)


@click.command()
@click.version_option(_version.__version__)
@click.option(
    '--out-path',
    'output_ht_path',
    required=True,
    help='VQSR filtering annotation resource',
)
@click.option(
    '--vqsr-vcf-path',
    'vqsr_vcf_path',
    help='Path to VQSR site-only VCF. Can be specified as Hadoop glob patterns',
)
@click.option(
    '--n-partitions',
    'n_partitions',
    help='Desired base number of partitions for output tables',
    default=1000,
    type=click.INT,
)
@click.option(
    '--bucket',
    'work_bucket',
    required=True,
    help='path to write intermediate output and checkpoints. '
    'Can be a Google Storage URL (i.e. start with `gs://`).',
)
@click.option(
    '--local-tmp-dir',
    'local_tmp_dir',
    help='local directory for temporary files and Hail logs (must be local).',
)
@click.option(
    '--overwrite',
    'overwrite',
    is_flag=True,
    help='if an intermediate or a final file exists, skip running the code '
    'that generates it.',
)
def main(  # pylint: disable=missing-function-docstring
    output_ht_path: str,
    vqsr_vcf_path: str,
    n_partitions: int,
    work_bucket: str,  # pylint: disable=unused-argument
    local_tmp_dir: str,
    overwrite: bool,
):
    utils.init_hail('load_data', local_tmp_dir)
    load_vqsr(
        vqsr_vcf_path, 
        output_ht_path,
        overwrite=overwrite,
        n_partitions=n_partitions,
    )


def load_vqsr(
    site_only_vqsr_vcf_path: str,
    output_ht_path: str,
    overwrite: bool = False,
    n_partitions: int = None,
):
    """
    Loads the VQSR'ed site-only VCF into a site-only hail table. Populates ht.filters
    """
    if utils.can_reuse(output_ht_path, overwrite):
        return hl.read_table(output_ht_path)

    logger.info(f'Importing VQSR annotations...')
    mt = hl.import_vcf(
        site_only_vqsr_vcf_path,
        force_bgz=True,
        reference_genome='GRCh38',
    )
    if n_partitions:
        mt = mt.repartition(n_partitions)

    ht = mt.rows()

    # some numeric fields are loaded as strings, so converting them to ints and floats 
    ht = ht.annotate(
        info=ht.info.annotate(
            AS_VQSLOD=ht.info.AS_VQSLOD.map(hl.float),
            AS_SB_TABLE=ht.info.AS_SB_TABLE.split(r'\|').map(
                lambda x: hl.if_else(
                    x == '', hl.missing(hl.tarray(hl.tint32)), x.split(',').map(hl.int)
                )
            ),
        ),
    )
    unsplit_count = ht.count()

    ht = hl.split_multi_hts(ht)
    ht = ht.annotate(
        info=ht.info.annotate(**split_info_annotation(ht.info, ht.a_index)),
    )
    ht = ht.annotate(
        filters=ht.filters.union(hl.set([ht.info.AS_FilterStatus])),
    )
    ht.write(output_ht_path, overwrite=True)
    ht = hl.read_table(output_ht_path)
    logger.info(f'Wrote split HT to {output_ht_path}')
    split_count = ht.count()
    logger.info(
        f'Found {unsplit_count} unsplit and {split_count} split variants with VQSR annotations'
    )
    return ht


if __name__ == '__main__':
    main()  # pylint: disable=E1120
