import bcrypt
import hashlib


class Polycule(object):
    def __init__(self, db=None, id=None, graph=None, view_pass=None,
                 delete_pass=None, graph_hash=None):
        self._db = db
        self.id = id
        self.graph = graph
        self.view_pass = view_pass
        self.delete_pass = delete_pass
        self.graph_hash = graph_hash

    @classmethod
    def get(cls, db, graph_hash, password, force=False):
        if len(graph_hash) < 7:
            return None
        graph_hash = graph_hash + '_' * (40 - len(graph_hash))
        result = db.execute('select * from polycules where hash like ?', [
            graph_hash
        ])
        graph = result.fetchall()
        if len(graph) != 1:
            return None
        graph = graph[0]
        polycule = Polycule(
            db=db,
            id=graph[0],
            graph=graph[1],
            view_pass=graph[2],
            delete_pass=graph[3],
            graph_hash=graph[4])
        if not force and (
                polycule.view_pass is not None and
                not bcrypt.checkpw(password.encode('utf-8'),
                                   polycule.view_pass.encode('utf-8'))):
            raise Polycule.PermissionDenied
        return polycule

    @classmethod
    def create(cls, db, graph, raw_view_pass, raw_delete_pass):
        if raw_view_pass is not None:
            view_pass = bcrypt.hashpw(
                raw_view_pass.encode(), bcrypt.gensalt()).decode()
        else:
            view_pass = None
        if raw_delete_pass is not None:
            delete_pass = bcrypt.hashpw(
                raw_delete_pass.encode(), bcrypt.gensalt()).decode()
        else:
            delete_pass = None
        result = db.execute('select count(*) from polycules where graph = ?',
                            [graph])
        existing = result.fetchone()[0]
        if existing != 0:
            raise Polycule.IdenticalGraph
        cur = db.cursor()
        result = cur.execute('''insert into polycules
            (graph, view_pass, delete_pass, hash) values (?, ?, ?, ?)''', [
                graph,
                view_pass,
                delete_pass,
                hashlib.sha1(graph.encode('utf-8')).hexdigest(),
            ])
        db.commit()
        new_hash = db.execute('select hash from polycules where id = ?', [
            result.lastrowid
        ]).fetchone()[0]
        return Polycule.get(db, new_hash, None, force=True)

    def delete(self, password, force=False):
        if not force and not bcrypt.checkpw(password.encode('utf-8'),
                                            self.delete_pass.encode('utf-8')):
            raise Polycule.PermissionDenied
        cur = self._db.cursor()
        cur.execute('delete from polycules where id = ?', [self.id])
        self._db.commit()

    class PermissionDenied(Exception):
        pass

    class IdenticalGraph(Exception):
        pass
