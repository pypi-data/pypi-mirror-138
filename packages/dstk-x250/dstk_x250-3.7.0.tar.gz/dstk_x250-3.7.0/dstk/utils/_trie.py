#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Structure graphe de type trie
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Created on Sun Feb 13 14:52:34 2022

@author: Cyrile Delestre
"""

from __future__ import annotations
from typing import Any, Dict
from functools import reduce

class Trie(dict):
    r"""
    Arbre simple de type trie construit sur la base des dictionnaires Python.
    Permet de construire des arbres et la gestion des noeuds manquants ce
    fait de manière transparente. Il est possible de bloquer la strcuture
    afin de figer le trie.

    Examples
    --------
    >>> from dstk.utils import Trie
    >>> 
    >>> trie = Trie()
    >>> trie.default_fields = dict(loss=None, val='test')
    >>> trie
        {}
    >>> trie['a']['b']['c'] = 42
    >>> trie
        {
            'a': {
                'loss': None,
                'val': 'test',
                'b': {
                    'c': 42
                }
            }
        }
    >>> 
    >>> trie.insert(*"cd", q=42)
    >>> trie
        {
            'a': {
                'loss': None,
                'val': 'test',
                'b': {
                    'c': 42
                }
            },
            'c': {
                'loss': None,
                'val': 'test',
                'd': {
                    'q': 42
                }
            }
        }
    >>> 
    >>> trie.lock
    >>> trie['q']
        KeyError: "La clef q n'existe pas."

    Warnings
    --------
    La valeur par défaut des noeuds est un dictionnaire vide, penser à faire :

    >>> trie.default_fields = dict(...)

    pour chancher ce comportement.
    """
    _lock: bool = False
    _default_fields = dict()

    def __missing__(self, key: Any) -> Trie:
        r"""
        Permet de créer un noeud de type Trie si l'instance n'existe pas.
        Méthode facile pour créer un arbre.

        Parameters
        ----------
        key: Any
            clef d'accès à l'instance du dictionnaire.
        """
        if not self._lock:
            val = self[key] = self.__class__(**self.default_fields)
            return val
        raise KeyError(f"La clef {key} n'existe pas.")

    def __setitem__(self, key, v):
        r"""
        Méthode interne d'insertion dans un dictionnaire et permet de passer
        le filtre de verrouillage du graphe ou non.
        """
        if not self._lock:
            super().__setitem__(key, v)
        else:
            raise KeyError(f"La clef {key} n'existe pas.")

    @property
    def default_fields(self) -> Dict[str, Any]:
        r"""
        Accesseur aux champs par défaut à chaque nouveau Noeud de l'arbre.
        """
        return self._default_fields

    @default_fields.setter
    def default_fields(self, kargs):
        r"""
        Permet de modier les champs par défaut à chaque nouveau Noeud du Trie.
        """
        self._default_fields = kargs

    @property
    def lock(self):
        r"""
        Permet de vérouille la construction du Trie.
        """
        self._lock = True
        if len(self) > 0:
            for key in self:
                if hasattr(self[key], '_lock'):
                    self[key].lock

    @property
    def unlock(self):
        r"""
        Permet de dévérouiller la construction du Trie.
        """
        self._lock = False
        if len(self) > 0:
            for key in self:
                if hasattr(self[key], '_lock'):
                    self[key].unlock

    @classmethod
    def deep_init(cls, graph: Dict[str, Any]) -> Trie:
        r"""
        Méthode de classe permettant de créé un Trie a partir d'éléments
        encapsuler dans un dictionnaire.

        Parameters
        ----------
        graph: Dict[str, Any]
            Structure du graphe trie au format dictionnaire Python.
        """
        trie = cls(graph)
        trie._deep_init()
        return trie

    def _deep_init(self):
        r"""
        Méthode récurrente pour propager les objets Trie dans l'arborescence.
        """
        if len(self) > 0:
            for key in self:
                if isinstance(self[key], dict):
                    self[key] = self.__class__(self[key])
                    self[key]._deep_init()

    def islock(self) -> bool:
        r"""
        Méthode de test si le Trie est lock ou non.

        Warnings
        --------
        Ne vérifie pas en profondeur, test seulement la racine du Trie. On
        suppose le comportement homogène de la classe.
        """
        return self._lock

    def access(self, *args) -> Any:
        r"""
        Méthode d'accès rapide à un élément du Trie. Si le Trie est 
        dévérouillé et que les noeuds d'accès à l'élément n'existe pas il sera
        créé, sinon une erreur KeyError sera émis.

        *args
            itérateur des arguments d'accès.

        Example
        -------
        >>> trie['a']['b']['c']
        >>> 42

        est équivalent à

        >>> trie.access(*"abc")
        >>> 42
        """
        return reduce(lambda x, y: x[y], args[1:], self[args[0]])

    def insert(self, *args, **kargs) -> None:
        r"""
        Méthode facilitant l'incertion d'un élément dans le Trie. Si le Trie
        est dévérouillé et que l'insersion utilise des noeuds qui n'existent
        pas dans le Trie alors il sera créé, sinon une erreur KeyError sera
        émis.

        Parameters
        ----------
        idx: int
            Valeur à entré au niveau de la feuille (argument 'idx').
        loss: float
            Valeur de la fonction coût calculé par l'apprentissage 
            (argument 'loss').
        *args :
            itérateur des arguments d'accès.

        Example
        -------
        >>> trie['a']['b']['c']['idx'] = 42
        >>> trie['a']['b']['c']['loss'] = 0.42

        est équivalent à

        >>> trie.insert(*"abc", idx=42, loss=0.42)
        """
        leaf = self.access(*args)
        for kk, vv in kargs.items():
            leaf[kk] = vv
