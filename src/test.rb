# frozen_string_literal: true

require 'bundler'
Bundler.require(:http)

get '/' do
  'Hello, world!'
end
