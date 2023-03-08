# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 The HuggingFace Authors.

import logging
from typing import List

from libcommon.config import ProcessingGraphConfig
from libcommon.processing_graph import ProcessingStep
from libcommon.queue import Priority, Queue
from libcommon.simple_cache import get_cache_info_for_kind_minor_than_version


def refresh_cache(processing_steps: List[ProcessingStep], processing_graph_config: ProcessingGraphConfig) -> None:
    queue = Queue()
    for processing_step in processing_steps:
        current_version = processing_graph_config.specification[processing_step.cache_kind]["version"]
        cache_records = get_cache_info_for_kind_minor_than_version(processing_step.cache_kind, current_version)
        logging.info(
            f"processing_step={processing_step.cache_kind} current_version={current_version} number_of_outdated_cache_records={len(cache_records)}"
        )
        for cache_info in cache_records:
            logging.debug(
                "upsert_job for"
                f" processing_step={processing_step.job_type} dataset={cache_info['dataset']} config={cache_info['config']} split={cache_info['split']}"
            )
            queue.upsert_job(
                job_type=processing_step.job_type,
                dataset=cache_info["dataset"],
                config=cache_info["config"],
                split=cache_info["split"],
                force=True,
                priority=Priority.LOW,
            )
