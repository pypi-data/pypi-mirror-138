"""Repository management for the Human Disease Ontology."""

import os
from git import Repo
from tqdm import tqdm

from . import owl


class DOrepo(Repo):
    """A class for the Human Disease Ontology repository."""

    def __init__(self, path):
        super().__init__(path)
        self.path = os.path.dirname(self.git_dir)
        self._onto_dir = os.path.join(self.path, "src", "ontology")
        self.doid_edit = owl.functional(os.path.join(self._onto_dir, "doid-edit.owl"))
        # self.doid = owl.xml(os.path.join(self._onto_dir, "doid.owl"))
        # self.doid_merged = owl.xml(os.path.join(self._onto_dir, "doid-merged.owl"))

    def tag_iterate(self, fxn, start = None, end = None, *args, **kwargs):
        if self.head.is_detached:
            initial_head = self.head.commit
        else:
            initial_head = self.head.ref

        tags = sorted(self.tags, key=lambda t: t.commit.committed_datetime)
        t_name = [t.name for t in tags]
        if start is None:
            start = t_name[0]
        if end is None:
            end = t_name[-1]

        res = {}
        include = False
        tag_it = tqdm(
            tags[t_name.index(start):(t_name.index(end) + 1)],
            desc = "executing at..."#,
            unit = "tag"
        )
        for t in tag_it:
            self.git.checkout(t)
            res[t.name] = fxn(*args, **kwargs)

        self.git.checkout(initial_head)
        return res
