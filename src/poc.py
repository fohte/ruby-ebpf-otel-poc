from bcc import BPF
import os

b = BPF(src_file=os.path.join(os.path.dirname(__file__), "poc.bpf.c"))

b.attach_uprobe(
    name="/home/ec2-user/.rbenv/versions/3.4.1/lib/libruby.so.3.4",
    sym="rb_yjit_iseq_gen_entry_point",
    fn_name="trace_puts",
)

b.trace_print()
