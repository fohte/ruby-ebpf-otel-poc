from bcc import BPF
import os

b = BPF(src_file=os.path.join(os.path.dirname(__file__), "poc.bpf.c")

b.attach_uprobe(
    name="/home/ec2-user/.rbenv/versions/3.4.1/bin/ruby",
    sym="rb_io_puts",
    fn_name="trace_puts",
)

b.trace_print()
