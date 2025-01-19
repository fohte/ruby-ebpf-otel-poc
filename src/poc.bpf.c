#include <uapi/linux/ptrace.h>

enum metrics_t {
  GC = 0,
  YJIT = 1,
};

BPF_HASH(metric_map, u32, u64);

int trace_rb_gc_usdt(struct pt_regs *ctx) {
  u32 key = GC;
  u64 *count, zero = 0;

  count = metric_map.lookup_or_init(&key, &zero);
  (*count)++;

  return 0;
}

int trace_rb_yjit(struct pt_regs *ctx) {
  u32 key = YJIT;
  u64 *count, zero = 0;

  count = metric_map.lookup_or_init(&key, &zero);
  (*count)++;

  return 0;
}
