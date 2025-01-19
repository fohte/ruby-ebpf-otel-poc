int trace_rb_method_entry(struct pt_regs *ctx) {
  bpf_trace_printk("method called [usdt]\n");
  return 0;
}

int trace_rb_method_return(struct pt_regs *ctx) {
  bpf_trace_printk("method returned [usdt]\n");
    char class_name[128] = {};
    char method_name[128] = {};

    u64 class_ptr = 0;
    u64 method_ptr = 0;

    bpf_usdt_readarg(1, ctx, &class_ptr);
    bpf_usdt_readarg(2, ctx, &method_ptr);

    if (class_ptr != 0) {
        bpf_probe_read_str(&class_name, sizeof(class_name), (void *)class_ptr);
    }
    if (method_ptr != 0) {
        bpf_probe_read_str(&method_name, sizeof(method_name), (void *)method_ptr);
    }

    bpf_trace_printk("Method returned: %s", class_name);
    bpf_trace_printk("#%s\n", method_name);

  return 0;
}

int trace_rb_cmethod_entry(struct pt_regs *ctx) {
  bpf_trace_printk("cmethod called [usdt]\n");
  return 0;
}

int trace_rb_cmethod_return(struct pt_regs *ctx) {
  bpf_trace_printk("cmethod returned [usdt]\n");
  return 0;
}

int trace_rb_gc_usdt(struct pt_regs *ctx) {
  bpf_trace_printk("GC happened [usdt]\n");
  return 0;
}

int trace_rb_gc(struct pt_regs *ctx) {
  bpf_trace_printk("GC happened\n");
  return 0;
}

int trace_rb_puts(struct pt_regs *ctx) {
  bpf_trace_printk("puts called\n");
  return 0;
}
