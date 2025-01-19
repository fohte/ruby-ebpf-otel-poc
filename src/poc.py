from bcc import BPF, USDT
from time import sleep
import os

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
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
