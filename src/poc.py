from bcc import BPF, USDT
from time import sleep
import os

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import get_meter_provider, set_meter_provider

otlp_exporter = OTLPMetricExporter(
    endpoint="http://localhost:14317",
)

metric_reader = PeriodicExportingMetricReader(
    exporter=otlp_exporter,
    export_interval_millis=5000,
)

meter_provider = MeterProvider(metric_readers=[metric_reader])
set_meter_provider(meter_provider)

meter = get_meter_provider().get_meter("gc-meter")

counter = meter.create_counter(
    name="gc-counter",
    description="GC count",
    unit="1",
)
pid = int(os.popen("pidof ruby").read().strip())

usdt = USDT(pid=pid)
usdt.enable_probe(probe="gc__mark__begin", fn_name="trace_rb_gc_usdt")

b = BPF(
    src_file=os.path.join(os.path.dirname(__file__), "poc.bpf.c"),
    usdt_contexts=[usdt],
)

b.attach_uprobe(
    name="/home/ec2-user/.rbenv/versions/3.4.1/lib/libruby.so.3.4",
    sym="rb_yjit_iseq_gen_entry_point",
    fn_name="trace_rb_yjit",
)

print("Tracing... Hit Ctrl-C to end.")

metric_keys = {0: "GC", 1: "YJIT"}

print("Metrics:")

try:
    while True:
        metric_map = b["metric_map"]
        for k, v in metric_map.items():
            metric_key = metric_keys[k.value]
            print(f"{metric_key}: {v.value}\n")
            if metric_key == "GC":
                counter.add(v.value)
                b["metric_map"][k] = 0
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
