int trace_puts(void *ctx)
{
  bpf_trace_printk("puts called\n");
  return 0;
}
