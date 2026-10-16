#!/usr/bin/env ruby

###########################################################################
# usage: ruby scripts/gen_guidance.rb
# This script generates a YAML file containing guidance yaml for each class
# and datatype and its attributes in the XMI model.
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

  def serialize_datatype(xmi, dt_path)
    parsed = XMI_PARSE_CACHE.fetch(xmi)
    dt = resolve_packaged_datatype(parsed, dt_path)

    if dt && dt.name && dt.xmi_id
      ::Ea::Xmi::LiquidDrops::DataTypeDrop.new(dt, nil, parsed.drop_options)
    end
  end
end

def add_attributes(drop)
  attrs = []
  gen = drop && drop.generalization

  if gen
    Array(gen.owned_props).each do |prop|
      attrs << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    Array(gen.sorted_assoc_props).each do |prop|
      attrs << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    Array(gen.inherited_props).each do |prop|
      attrs << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    Array(gen.sorted_inherited_assoc_props).each do |prop|
      attrs << {
        'name' => "#{prop.name_ns}:#{prop.name}",
        'used' => false,
        'guidance' => "この属性は使用されていません。"
      }
    end
    return attrs
  end

  Array(drop.owned_attributes).map do |prop|
    attrs << {
      'name' => prop.name,
      'used' => false,
      'guidance' => "この属性は使用されていません。"
    }
  end
  attrs
end

def loop_thru(model, pathname: "::EA_Model", data: { 'classes' => [], 'data_types' => [] })
  Array(model.classes).each do |klass|
    # Interfaces/Signals/Components are not part of the guidance output;
    # only uml:Class and uml:AssociationClass resolve to a KlassDrop.
    next unless klass.name && klass.xmi_id
    next unless %w[Class AssociationClass].include?(klass.type)

    full_path = "#{pathname}::#{klass.name}"
    drop = Test.new.serialize_klass(File.expand_path(XMI_PATH), full_path)
    next unless drop

    klass_data = {
      'name' => full_path,
      'attributes' => add_attributes(drop)
    }

    puts "Processing class: #{full_path}"
    pp klass_data

    data['classes'] << klass_data
  end

  Array(model.data_types).each do |dt|
    next unless dt.name && dt.xmi_id

    full_path = "#{pathname}::#{dt.name}"
    drop = Test.new.serialize_datatype(File.expand_path(XMI_PATH), full_path)
    next unless drop

    dt_data = {
      'name' => full_path,
      'attributes' => add_attributes(drop)
    }

    puts "Processing datatype: #{full_path}"
    pp dt_data

    data['data_types'] << dt_data
  end

  Array(model.packages).each do |package|
    loop_thru(package, pathname: "#{pathname}::#{package.name}", data: data)
  end
end

def main
  root = ::Xmi::Sparx::Root.parse_xml(File.read(File.expand_path(XMI_PATH)))
  root_model = Ea::Xmi::Parser.new.parse(root)
  data = { 'classes' => [], 'data_types' => [] }

  loop_thru(root_model, pathname: "::EA_Model", data: data)

  File.write(File.expand_path(OUTPUT_PATH), data.to_yaml)
end

main
