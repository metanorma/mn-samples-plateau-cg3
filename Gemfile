source "https://rubygems.org"

gem "metanorma-cli", git: "https://github.com/metanorma/metanorma-cli", branch: "main" # fleet pins for the 1.3-era flavors
# metanorma 2.5.5 needs Metanorma::Core::Flavors; rubygems' metanorma-core 0.2.3 lacks it
gem "metanorma-core", git: "https://github.com/metanorma/metanorma-core", branch: "main"
gem "ffi"

gem "html2doc", git: "https://github.com/metanorma/html2doc", branch: "main"
gem "isodoc-i18n", git: "https://github.com/metanorma/isodoc-i18n", branch: "main"
gem "isodoc", git: "https://github.com/metanorma/isodoc", branch: "main"
gem "metanorma-standoc", git: "https://github.com/metanorma/metanorma-standoc", branch: "main" # #1269 merged: GC budget + partial-load preprocessor registration
gem "metanorma-document", git: "https://github.com/metanorma/metanorma-document", branch: "main"
gem "metanorma", git: "https://github.com/metanorma/metanorma", branch: "main"
gem "metanorma-iso", git: "https://github.com/metanorma/metanorma-iso", branch: "main" # iso#1653 merged (bounded GC window)
gem "metanorma-plateau", github: "metanorma/metanorma-plateau", branch: "main"
# utils#55: GcBudget + in-place asciidoctor table cell buffer (asciidoctor 2.0.x
# rebuilds the whole cell buffer per appended line = O(N^2); asciidoctor is
# third-party so the fix is carried in our gem, self-disarming at their fix)
gem "metanorma-utils", git: "https://github.com/metanorma/metanorma-utils", branch: "main" # utils#55 merged (GcBudget + table cell buffer); #56 pending
gem "mn-requirements", git: "https://github.com/metanorma/mn-requirements", branch: "main"
gem "debug"
gem "sassc-embedded"

# ogc/itu/ieee/iho carried relaton-render path-shadowing fixes (their
# lib/relaton/render/*.rb shadowed relaton-render's require paths and booted
# the deleted Render::Parse at boot). ogc#1014, itu#861, bipm#694 and
# iec#594 merged: on main. ieee#816 and iho#547 are still open: pinned at
# the shadowing fixes until they do
gem "metanorma-ogc", github: "metanorma/metanorma-ogc", branch: "main"
gem "metanorma-itu", github: "metanorma/metanorma-itu", branch: "main"
gem "metanorma-ieee", github: "metanorma/metanorma-ieee",
    ref: "6af0ea64a4444c7b201dedb7eb06e5bbceaa4f70" # metanorma-ieee#816 pending
gem "metanorma-iho", github: "metanorma/metanorma-iho",
    ref: "dfcc029ab2e83a1fe4248d382e71b85998275225" # metanorma-iho#547 pending
gem "metanorma-bipm", github: "metanorma/metanorma-bipm", branch: "main"
gem "metanorma-ietf", github: "metanorma/metanorma-ietf", branch: "main" # main replaced its relaton-render stack natively
# cli pulls iec transitively at 2.9.0, whose front.rb requires the removed
# standalone pubid-iec; iec main loads IEC identifiers through the pubid
# monogem instead (iec#594 merged)
gem "metanorma-iec", github: "metanorma/metanorma-iec", branch: "main"
gem "metanorma-jis", github: "metanorma/metanorma-jis", branch: "main"

# hyperperformance line: git-main for the whole lutaml family
gem "lutaml-model", github: "lutaml/lutaml-model", branch: "main"
gem "moxml", github: "lutaml/moxml", branch: "main" # moxml#324 merged: NodeSet set-ops + mutator adoption
gem "leptris", "1.9.317" # v1.9.304: leptris#1528 fixed (cross-document splice adoption); #1528 was the sectioned-cleanup segfault
gem "ea", "= 0.6.45" # released; Ea::Xmi partial loading (ea#86)
gem "xmi", github: "lutaml/xmi", branch: "main"
gem "metanorma-plugin-lutaml", github: "metanorma/metanorma-plugin-lutaml", branch: "main" # plugin#311 merged (0.7.54): partial load via lutaml-ea-xmi-load

# monogems: relaton + pubid at git main (the metanorma gems already depend on
# these names; released rubygems snapshots lag the monogem APIs)
# the plateau corpus stack: relaton alpha.4 fragment + relaton-render 1.3 line -
# the combination the citation rendering (site-gen) actually works with;
# relaton-render main dropped the flavor-render base classes (Render::I18n et al.)
gem "relaton", "= 3.0.0.pre.alpha.4"
gem "relaton-cli", github: "relaton/relaton", tag: "v3.0.0.pre.alpha.4", glob: "gems/relaton-cli/relaton-cli.gemspec" # the released gem declares pubid (~> 2.0.0.pre.alpha.13), a prerelease dep the rubygems API does not advertise — fresh installs fail the API check against pubid main; revisit when relaton-cli releases past it
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
gem "relaton-render", "= 3.0.0.pre.alpha.19" # released render-3x line: #111 i18n fallback, #115 per-item language, 1.x renderings contract restored
