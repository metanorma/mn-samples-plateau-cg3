source "https://rubygems.org"

# Every git gem below is pinned to the exact revision validated by the green
# docker workflow run 36686998573 (2026-09-30, render-datatype-tables @
# d1016052). Together with the committed Gemfile.lock this keeps CI
# reproducible — floating `branch: "main"` deps previously broke the
# deployment when upstream changed (issue #14).

gem "metanorma-cli"
gem "ffi"

gem "html2doc", github: "metanorma/html2doc", ref: "4b54dfaf9c96ec6535fed2847bed1c37aa64c49b"
gem "isodoc-i18n", github: "metanorma/isodoc-i18n", ref: "2f8c4e53d1f14778a08dbd43a7a255100aacc329"
# feat/extend-lutaml-klass-table as of the green run
gem "metanorma-plugin-lutaml", github: "metanorma/metanorma-plugin-lutaml", ref: "98a37630d63c787a96400c31be5a63e1d0554e5c"

# Pin ref of the gem relaton-render to commit 932b921 to
# fix uninitialized constant Relaton::Render::General (NameError)
gem "relaton-render", github: "relaton/relaton-render", ref: "932b921"

# feat/flavor-table as of the green run (fixes flavor table issue in
# metanorma-core; iso main registers flavors via Metanorma::Core::Flavors)
gem "metanorma-core", github: "metanorma/metanorma-core", ref: "2769a00c38dcb47a457a833471cb991c53ec4f75"

gem "metanorma-utils", github: "metanorma/metanorma-utils", ref: "5fda52af4a09cd3492911beb192e71879659491f"
gem "metanorma-jis", github: "metanorma/metanorma-jis", ref: "d4f18b93d68b96b2a32b69b35ba95a4594106a30"
gem "metanorma-itu", github: "metanorma/metanorma-itu", ref: "ac05b328e2de1880d88433d3467db215e20378f9"
gem "metanorma-iec", github: "metanorma/metanorma-iec", ref: "988fb3bca05eb3286e23783a1e7898f1a4aaa06b"
gem "metanorma-ieee", github: "metanorma/metanorma-ieee", ref: "e8f24ab637657fd7b2f31c09979a61e1c150b9a1"
gem "metanorma-plateau", github: "metanorma/metanorma-plateau", ref: "6224318a92cd6b3f623455d643dbb418703e0ed0"
gem "metanorma-iso", github: "metanorma/metanorma-iso", ref: "9b262b719d50f08c3e39bb316c60b4902d216375"
gem "isodoc", github: "metanorma/isodoc", ref: "d75b68711b01b548aad85cf378bee532d02cd945"

# TEMPORARY: cross-PR branch pins so CI can resolve the in-flight
# metanorma-standoc namespace rename (Metanorma::Standoc::Document)
# and the pubid-2 / relaton-bib 2.2 / metanorma-document 0.5 chain.
# Revert each pin once the corresponding PR merges:
#   - https://github.com/metanorma/metanorma-standoc/pull/1232
#   - https://github.com/metanorma/metanorma-document/pull/45
gem "metanorma-standoc", github: "metanorma/metanorma-standoc", ref: "ec98d74da0d260fd77557e2f04a20884f6d4a2c7"
gem "metanorma-document", github: "metanorma/metanorma-document", ref: "d1ff9f06b72b1daccfab54799286777a05c8b22b"

# Fix pubid v2 issues
gem "relaton", "= 3.0.0.pre.alpha.4"
gem "pubid", "= 2.0.0.pre.alpha.13"

# Exact versions from the green run — later releases broke the build
gem "lutaml-model", "= 0.8.85"
gem "moxml", "= 0.5.96"
gem "leptris", "= 1.9.273.1"
gem "yeptris", "= 0.6.26.2", force_ruby_platform: true
gem "ea", "= 0.6.12"
gem "expressir", "= 2.4.27"
gem "glossarist", "= 2.14.0"
gem "lutaml-hal", "= 0.2.5"
gem "lutaml-lml", "= 0.1.5"
gem "lutaml-store", "= 0.2.4"
gem "parsanol", "= 1.3.56"
gem "tzinfo-data", "= 1.2026.4"
gem "word-to-markdown", "= 1.2.0"

gem "sassc-embedded"
gem "debug"
gem "irb"
