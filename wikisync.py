import os
import igem_wikisync as sync

sync.run(
    team      = os.environ.get('WIKISYNC_TEAM'),
    src_dir   = os.environ.get('WIKISYNC_SOURCE'),
    build_dir = os.environ.get('WIKISYNC_BUILD'),
    poster_mode = os.environ.get('WIKISYNC_POSTER')
)
