# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 The HuggingFace Authors.

import os
import re
from typing import Mapping

from .utils import API_URL, get


def has_metric(name: str, labels: Mapping[str, str], metrics: set[str]) -> bool:
    label_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
    s = name + "{" + label_str + "}"
    return any(re.match(s, metric) is not None for metric in metrics)


def test_metrics():
    assert "PROMETHEUS_MULTIPROC_DIR" in os.environ
    response = get("/metrics", url=API_URL)
    assert response.status_code == 200, f"{response.status_code} - {response.text}"
    content = response.text
    lines = content.split("\n")
    metrics = {line.split(" ")[0]: float(line.split(" ")[1]) for line in lines if line and line[0] != "#"}
    # see https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn
    assert "process_start_time_seconds" not in metrics

    # the middleware should have recorded the request
    name = 'starlette_requests_total{method="GET",path_template="/metrics"}'
    assert name in metrics, metrics
    assert metrics[name] > 0, metrics

    metrics = set(metrics.keys())
    for endpoint in ["/splits", "/first-rows", "/parquet"]:
        # these metrics are only available in the admin API
        assert not has_metric(
            name="queue_jobs_total", labels={"pid": "[0-9]*", "queue": endpoint, "status": "started"}, metrics=metrics
        ), f"queue_jobs_total - endpoint={endpoint} found in {metrics}"
        assert not has_metric(
            name="responses_in_cache_total",
            labels={"error_code": "None", "http_status": "200", "path": endpoint, "pid": "[0-9]*"},
            metrics=metrics,
        ), f"responses_in_cache_total - endpoint {endpoint} found in {metrics}"
