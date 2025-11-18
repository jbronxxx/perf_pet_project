import time

from flask import Flask, Response, g, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "Latency of HTTP requests in seconds.", ["method", "path"]
)

REQUEST_COUNT = Counter(
    "http_requests_total", "Total number of HTTP requests.", ["method", "path", "status_code"]
)


def start_timer() -> None:
    """Starts a timer at the beginning of a request."""
    # Use Flask's 'g' object to store the start time.
    # 'g' is a request-bound global context that is safe to use for this purpose.
    g.start_time = time.time()


def stop_timer(response: Response) -> Response:
    """Stops the timer and records RED metrics at the end of a request."""
    # Calculate total request processing time.
    resp_time = time.time() - g.start_time

    # Get the URL rule for the path template (e.g., '/products/<int:id>').
    # This avoids high cardinality issues with dynamic path parameters.
    path_template = request.url_rule.rule if request.url_rule else request.path

    # Record the latency in the histogram.
    REQUEST_LATENCY.labels(method=request.method, path=path_template).observe(resp_time)

    # Increment the request counter.
    REQUEST_COUNT.labels(
        method=request.method, path=path_template, status_code=response.status_code
    ).inc()

    return response


def metrics_endpoint() -> Response:
    """Generates the Prometheus metrics report."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


def register_metrics(app: Flask) -> None:
    """Registers the metrics collection hooks with a Flask app.

    Args:
        app: The Flask application instance.
    """
    # Run start_timer before each request.
    app.before_request(start_timer)
    # Run stop_timer after each request.
    app.after_request(stop_timer)
    # Add the /metrics endpoint to expose the metrics.
    app.add_url_rule("/metrics", "metrics", metrics_endpoint)
