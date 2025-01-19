from bcc import BPF, USDT
import os

pid = int(os.popen("pidof ruby").read().strip())

usdt = USDT(pid=pid)
usdt.enable_probe(probe="gc__mark__begin", fn_name="trace_rb_gc_usdt")
usdt.enable_probe(probe="method__entry", fn_name="trace_rb_method_entry")
usdt.enable_probe(probe="method__return", fn_name="trace_rb_method_return")
# usdt.enable_probe(probe="cmethod__entry", fn_name="trace_rb_cmethod_entry")
# usdt.enable_probe(probe="cmethod__return", fn_name="trace_rb_cmethod_return")

b = BPF(
    src_file=os.path.join(os.path.dirname(__file__), "poc.bpf.c"),
    usdt_contexts=[usdt],
)

b.attach_uprobe(
    name="/home/ec2-user/.rbenv/versions/3.4.1/lib/libruby.so.3.4",
    sym="rb_gc_start",
    fn_name="trace_rb_gc",
)

b.attach_uprobe(
    name="/home/ec2-user/.rbenv/versions/3.4.1/lib/libruby.so.3.4",
    sym="rb_io_puts",
    fn_name="trace_rb_puts",
)

print("Tracing... Hit Ctrl-C to end.")
b.trace_print()
