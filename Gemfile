source "https://rubygems.org"

gem "metanorma-cli", git: "https://github.com/metanorma/metanorma-cli", branch: "main" # fleet pins for the 1.3-era flavors
# metanorma 2.5.5 needs Metanorma::Core::Flavors; rubygems' metanorma-core 0.2.3 lacks it
gem "metanorma-core", git: "https://github.com/metanorma/metanorma-core", branch: "main"
gem "ffi"

gem "html2doc", git: "https://github.com/metanorma/html2doc", branch: "main"
gem "isodoc-i18n", git: "https://github.com/metanorma/isodoc-i18n", branch: "main"
gem "isodoc", git: "https://github.com/metanorma/isodoc", branch: "main"
gem "metanorma-standoc", git: "https://github.com/metanorma/metanorma-standoc", branch: "perf/cleanup-gc-budget" # #1266 sectioned-semantic + #1269 GcBudget + XmiSlices registration
gem "metanorma-document", git: "https://github.com/metanorma/metanorma-document", branch: "main"
gem "metanorma", git: "https://github.com/metanorma/metanorma", branch: "main"
gem "metanorma-iso", git: "https://github.com/metanorma/metanorma-iso", branch: "perf/validate-gc-budget" # iso#1653: bounded GC window in asset_style
gem "metanorma-plateau", git: "https://github.com/metanorma/metanorma-plateau", branch: "fix/lazy-load-relaton-render" # metanorma-plateau#407
# utils#55: GcBudget + in-place asciidoctor table cell buffer (asciidoctor 2.0.x
# rebuilds the whole cell buffer per appended line = O(N^2); asciidoctor is
# third-party so the fix is carried in our gem, self-disarming at their fix)
gem "metanorma-utils", git: "https://github.com/metanorma/metanorma-utils", branch: "perf/asciidoctor-table-buffer"
gem "mn-requirements", git: "https://github.com/metanorma/mn-requirements", branch: "main"
gem "debug"
gem "sassc-embedded"

# ogc/itu/ieee/iho main carry the relaton-render path-shadowing fixes (their
# lib/relaton/render/*.rb shadowed relaton-render's require paths and booted
# the deleted Render::Parse at boot: metanorma-ogc#1014, metanorma-itu#861,
# metanorma-ieee#816, metanorma-iho#547); flip these pins to branch: "main"
# once they merge
gem "metanorma-ogc", github: "metanorma/metanorma-ogc",
    ref: "3e27e9f87b4300d8995ea9a3d98b10b8d82d0c17"
gem "metanorma-itu", github: "metanorma/metanorma-itu",
    ref: "eceb3fbd7720c179ad534c3a26b5a762fbde0f6f"
gem "metanorma-ieee", github: "metanorma/metanorma-ieee",
    ref: "6af0ea64a4444c7b201dedb7eb06e5bbceaa4f70"
gem "metanorma-iho", github: "metanorma/metanorma-iho",
    ref: "dfcc029ab2e83a1fe4248d382e71b85998275225" # metanorma-iho#547
gem "metanorma-bipm", github: "metanorma/metanorma-bipm",
    ref: "43b63a2346d4d9b22c966e0d7a5e0e3c7251ec60" # metanorma-bipm#694
gem "metanorma-ietf", github: "metanorma/metanorma-ietf", branch: "main" # main replaced its relaton-render stack natively
# cli pulls iec transitively at 2.9.0, whose front.rb requires the removed
# standalone pubid-iec; iec main loads IEC identifiers through the pubid
# monogem instead
gem "metanorma-iec", github: "metanorma/metanorma-iec",
    ref: "79d56ed6f969f5b52e9240a42ed77ee230e158c1" # metanorma-iec#594
gem "metanorma-jis", git: "https://github.com/metanorma/metanorma-jis", branch: "fix/lazy-load-relaton-render" # stacked on PR 523 (1.2.1 + pubid unpin); metanorma-jis#525

# hyperperformance line: git-main for the whole lutaml family
gem "lutaml-model", github: "lutaml/lutaml-model", branch: "main"
gem "moxml", github: "lutaml/moxml", branch: "perf/node-set-intersection" # NodeSet set-ops + mutator adoption (moxml#317 line), unreleased at 0.5.105
gem "leptris", "1.9.304" # v1.9.304: leptris#1528 fixed (cross-document splice adoption); #1528 was the sectioned-cleanup segfault
gem "ea", github: "lutaml/ea", branch: "perf/xmi-slicer" # Ea::Xmi::Slicer
gem "xmi", github: "lutaml/xmi", branch: "main"
gem "metanorma-plugin-lutaml", github: "metanorma/metanorma-plugin-lutaml", branch: "perf/xmi-slices" # per-class XMI slices (:lutaml-xmi-slices:)

# monogems: relaton + pubid at git main (the metanorma gems already depend on
# these names; released rubygems snapshots lag the monogem APIs)
# the plateau corpus stack: relaton alpha.4 fragment + relaton-render 1.3 line -
# the combination the citation rendering (site-gen) actually works with;
# relaton-render main dropped the flavor-render base classes (Render::I18n et al.)
gem "relaton", "= 3.0.0.pre.alpha.4"
gem "relaton-cli", github: "relaton/relaton", tag: "v3.0.0.pre.alpha.4", glob: "gems/relaton-cli/relaton-cli.gemspec"
gem "pubid", github: "pubid/pubid", branch: "main"
# relaton-render main: the ISO 690 rewrite line; light deps (relaton became a
# development dependency), so it coexists with the relaton monogem. The
# released 1.3 line still pulls the relaton-bib fragment, whose
# Relaton::RequestError redefinition clashes with the monogem.
# relaton-render 1.3 line: render main dropped Render::General that the flavor
# stacks subclass; released 1.3 has it and coexists with the fragment relaton.
# PINNED to = 1.3.0: unpinned, the resolver grabs the 3.0.0 pre-alphas, which
# also dropped Render::I18n (metanorma-plateau's render-plateau/i18n.rb
# subclasses it -> NameError: uninitialized constant Relaton::Render::I18n)
gem "relaton-render", "= 1.3.0"
