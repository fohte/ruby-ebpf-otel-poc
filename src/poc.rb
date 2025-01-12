# frozen_string_literal: true

require 'bundler'
Bundler.require(:bpf)

include RbBCC

b = BCC.new(src_file: "#{__dir__}/poc.bpf.c")

b.trace_print
