#!/usr/bin/env ruby
# frozen_string_literal: true

###########################################################################
# usage:
#   bundle exec ruby scripts/gen_xmi_models.rb
#   bundle exec ruby scripts/gen_xmi_models.rb -i path/to/file.xmi -t datatype -o output.txt
#
# Parses an EA XMI export and writes fully qualified element names
# (parent packages + element name), one per line. For example:
#   Model::CityGML::Appearance::AbstractTexture
###########################################################################

require "optparse"
require "lutaml/uml"
require "ea/xmi"

DEFAULT_INPUT = "sources/xmi/plateau_all_packages_export.xmi"
DEFAULT_OUTPUT = "output.txt"
DEFAULT_TYPE = "class"

options = {
  input: DEFAULT_INPUT,
  output: DEFAULT_OUTPUT,
  type: DEFAULT_TYPE,
}

OptionParser.new do |opts|
  opts.banner = "Usage: ruby scripts/gen_xmi_models.rb [options]"

  opts.on("-i", "--input PATH", "XMI input file (default: #{DEFAULT_INPUT})") do |v|
    options[:input] = v
  end

  opts.on("-t", "--type TYPE", %w[class datatype],
          "Element type to collect: class or datatype (default: #{DEFAULT_TYPE})") do |v|
    options[:type] = v
  end

  opts.on("-o", "--output PATH", "Output text file (default: #{DEFAULT_OUTPUT})") do |v|
    options[:output] = v
  end

  opts.on("-h", "--help", "Show this help") do
    puts opts
    exit
  end
end.parse!

input_path = File.expand_path(options[:input])
unless File.file?(input_path)
  warn "Input XMI file not found: #{input_path}"
  exit 1
end

def elements_for(package, type)
  case type
  when "datatype"
    Array(package.data_types)
  else
    Array(package.classes)
  end
end

def collect_names(package, parent_path, type, results)
  package_path = [parent_path, package.name].compact.reject(&:empty?)
  full_prefix = package_path.join("::")

  elements_for(package, type).each do |element|
    next unless element&.name

    results << [full_prefix, element.name].reject(&:empty?).join("::")
  end

  Array(package.packages).each do |sub_package|
    collect_names(sub_package, full_prefix, type, results)
  end
end

root = ::Ea::Xmi::Parser.serialize_to_liquid(input_path)
results = []

Array(root.packages).each do |package|
  collect_names(package, "", options[:type], results)
end

output_path = File.expand_path(options[:output])
File.write(output_path, results.join("\n") + (results.empty? ? "" : "\n"))

puts "Wrote #{results.size} #{options[:type]} name(s) to #{output_path}"
