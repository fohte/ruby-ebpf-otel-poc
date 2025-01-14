# frozen_string_literal: true

require 'bundler'
Bundler.require(:bpf)

include RbBCC # rubocop:disable Style/MixinUsage

b = BCC.new(src_file: "#{__dir__}/poc.bpf.c")

b.attach_uprobe(
  sym: 'rb_io_puts',
  fn_name: 'trace_puts',
)

b.trace_print
