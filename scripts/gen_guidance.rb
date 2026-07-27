#!/usr/bin/env ruby

###########################################################################
# usage: ruby scripts/gen_guidance.rb
# This script generates a YAML file containing guidance yaml for each class
# and its attributes in the XMI model.
###########################################################################

require "metanorma-plugin-lutaml"
require "xmi"
require 'yaml'

XMI_PATH = "sources/xmi/plateau_all_packages_export.xmi"
OUTPUT_PATH = "sources/guidance/guidance_full.yaml"

class Test
  include Metanorma::Plugin::Lutaml::XmiCache

  def serialize_klass(xmi, klass_path)
    parsed = XMI_PARSE_CACHE.fetch(xmi)
    klass = resolve_packaged_klass(parsed, klass_path)

    if klass && klass.name && klass.xmi_id
      ::Ea::Xmi::LiquidDrops::KlassDrop.new(klass, nil, parsed.drop_options)
    end
  end
end

def add_attributes_to_klass(klass_path)
  klass = Test.new.serialize_klass(File.expand_path(XMI_PATH), klass_path)
  attr = []

  if klass && klass.name && klass.generalization
    klass.generalization.inherited_props.each do |prop|
      attr << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    klass.generalization.owned_props.each do |prop|
      attr << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    klass.generalization.sorted_inherited_assoc_props.each do |prop|
      attr << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    klass.generalization.sorted_assoc_props.each do |prop|
      attr << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
  end

  attr
end

def loop_thru(model, pathname: "::EA_Model", data: { 'classes' => [] })
  model.classes.each do |klass|
    if klass.name && klass.xmi_id && klass.generalization
      full_path = "#{pathname}::#{klass.name}"

      klass_data = {
        'name' => full_path,
        'attributes' => add_attributes_to_klass(full_path)
      }

      puts "Processing class: #{full_path}"
      pp klass_data

      data['classes'] << klass_data
    end
  end

  model.packages.each do |package|
    loop_thru(package, pathname: "#{pathname}::#{package.name}", data: data)
  end
end

def main
  root = ::Xmi::Sparx::Root.parse_xml(File.read(File.expand_path(XMI_PATH)))
  root_model = Ea::Xmi::Parser.new.parse(root)
  data = { 'classes' => [] }

  loop_thru(root_model, pathname: "::EA_Model", data: data)

  File.write(File.expand_path(OUTPUT_PATH), data.to_yaml)
end

main