("Hissp's basic macros.\n"
 '\n'
 "The basic macros are just enough to test and demonstrate Hissp's macro\n"
 'system; they are not intended to be a standard library for general use,\n'
 'but may suffice for small projects.\n'
 '\n'
 'As a convenience, they are automatically made available unqualified in\n'
 'the Lissp REPL, but this does not apply to modules. (A Hissp module with\n'
 'better alternatives need not use the basic macros at all.) In modules,\n'
 'either use the fully-qualified names, or start with the `prelude` macro.\n'
 '\n'
 'You can abbreviate qualifiers with the `alias` macro:\n'
 '\n'
 '.. code-block:: Lissp\n'
 '\n'
 '  (hissp.basic.._macro_.alias b/ hissp.basic.._macro_.)\n'
 '  ;; Now the same as (hissp.basic.._macro_.define foo 2).\n'
 '  (b/#define foo 2)\n'
 '\n'
 'The basic macros are deliberately restricted in design.\n'
 '\n'
 'They have NO DEPENDENCIES in their expansions; they use only the\n'
 'standard library with no extra helper functions. This means that all\n'
 'helper code must be inlined, resulting in larger expansions than might\n'
 'otherwise be necessary. But because macros expand before run time, the\n'
 'compiled code does not require Hissp to be installed to work.\n'
 '\n'
 'They also have no prerequisite initialization, beyond what is available\n'
 'in a standard Python module. For example, a ``_macro_`` namespace need\n'
 "not be available for ``defmacro``. It's smart enough to check for the\n"
 'presence of ``_macro_`` in its expansion context, and inline the\n'
 'initialization code when required.\n'
 '\n'
 'With the exception of `prelude` (which uses `exec`), they also eschew\n'
 'any expansions to Python code, relying only on the built-in special\n'
 'forms ``quote`` and ``lambda``, which makes their expansions compatible\n'
 'with advanced rewriting macros that process the Hissp expansions of\n'
 'other macros.\n'
 '\n'
 'To help keep macro definitions and expansions manageable in complexity,\n'
 'these basic macros lack some of the extra features their equivalents\n'
 'have in Python or in other Lisps.\n')

globals().update(
  _macro_=__import__('types').ModuleType(
            ('{}._macro_').format(
              __name__)))

__import__('operator').setitem(
  __import__('sys').modules,
  _macro_.__name__,
  _macro_)

setattr(
  _macro_,
  'defmacro',
  (lambda name,parameters,docstring,*body:
    (lambda * _: _)(
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          '_G_QzNo1_',
          (lambda * _: _)(
            'lambda',
            parameters,
            *body)),
        (lambda * _: _)(
          'builtins..setattr',
          '_G_QzNo1_',
          (lambda * _: _)(
            'quote',
            '__doc__'),
          docstring),
        (lambda * _: _)(
          'builtins..setattr',
          '_G_QzNo1_',
          (lambda * _: _)(
            'quote',
            '__qualname__'),
          (lambda * _: _)(
            '.join',
            "('.')",
            (lambda * _: _)(
              'quote',
              (lambda * _: _)(
                '_macro_',
                name)))),
        (lambda * _: _)(
          'builtins..setattr',
          'hissp.basic.._macro_',
          (lambda * _: _)(
            'quote',
            name),
          '_G_QzNo1_')))))

# defmacro
(lambda _G_QzNo1_=(lambda test,then,otherwise:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      (lambda * _: _)(
        'test',
        ':',
        ':*',
        'thenQz_else'),
      (lambda * _: _)(
        (lambda * _: _)(
          'operator..getitem',
          'thenQz_else',
          (lambda * _: _)(
            'operator..not_',
            'test')))),
    test,
    (lambda * _: _)(
      'lambda',
      ':',
      then),
    (lambda * _: _)(
      'lambda',
      ':',
      otherwise))):(
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__doc__',
    ('``if-else`` Basic ternary branching construct.\n'
     '\n'
     "  Like Python's conditional expressions, the 'else' clause is required.\n"
     '  ')),
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'ifQz_else',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'ifQz_else',
    _G_QzNo1_))[-1])()

# defmacro
(lambda _G_QzNo1_=(lambda *body:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      ':',
      *body))):(
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__doc__',
    ('Evaluates each body expression in sequence (for side effects),\n'
     '  resulting in the value of the last (or ``()`` if empty).\n'
     '  ')),
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'progn',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'progn',
    _G_QzNo1_))[-1])()

# defmacro
(lambda _G_QzNo1_=(lambda condition,*body:
  (lambda * _: _)(
    'hissp.basic.._macro_.ifQz_else',
    condition,
    (lambda * _: _)(
      'hissp.basic.._macro_.progn',
      *body),
    ())):(
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__doc__',
    ('When the condition is true,\n'
     '  evaluates each expression in sequence for side effects,\n'
     '  resulting in the value of the last.\n'
     '  Otherwise, skips them and returns ``()``.\n'
     '  ')),
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'when',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'when',
    _G_QzNo1_))[-1])()

# defmacro
(lambda _G_QzNo1_=(lambda condition,*body:
  (lambda * _: _)(
    'hissp.basic.._macro_.ifQz_else',
    condition,
    (),
    (lambda * _: _)(
      'hissp.basic.._macro_.progn',
      *body))):(
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__doc__',
    ('Unless the condition is true,\n'
     '  evaluates each expression in sequence for side effects,\n'
     '  resulting in the value of the last.\n'
     '  Otherwise, skips them and returns ``()``.\n'
     '  ')),
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'unless',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'unless',
    _G_QzNo1_))[-1])()

# defmacro
(lambda _G_QzNo1_=(lambda pairs,*body:
  (lambda * _: _)(
    (lambda * _: _)(
      'lambda',
      (lambda * _: _)(
        ':',
        *pairs),
      *body))):(
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__doc__',
    ('Creates local variables. Pairs are implied. Locals are not in scope until '
     'the body.')),
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'let',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'let',
    _G_QzNo1_))[-1])()

# defmacro
(lambda _G_QzNo1_=(lambda name,parameters,docstring=(),*body:
  # let
  (lambda QzDOLR_fn='_fn_QzNo7_':
    # let
    (lambda fn=(lambda * _: _)(
      'lambda',
      parameters,
      docstring,
      *body),ns=# unless
    # hissp.basic.._macro_.ifQz_else
    (lambda test,*thenQz_else:
      __import__('operator').getitem(
        thenQz_else,
        __import__('operator').not_(
          test))())(
      __import__('operator').contains(
        __import__('hissp.compiler',fromlist='?').NS.get(),
        '_macro_'),
      (lambda :()),
      (lambda :
        # hissp.basic.._macro_.progn
        (lambda :
          (lambda * _: _)(
            (lambda * _: _)(
              '.update',
              (lambda * _: _)(
                'builtins..globals'),
              ':',
              'hissp.basic.._macro_',
              (lambda * _: _)(
                'types..ModuleType',
                (lambda * _: _)(
                  'quote',
                  '_macro_')))))())),dc=# when
    # hissp.basic.._macro_.ifQz_else
    (lambda test,*thenQz_else:
      __import__('operator').getitem(
        thenQz_else,
        __import__('operator').not_(
          test))())(
      __import__('hissp.reader',fromlist='?').is_string(
        docstring),
      (lambda :
        # hissp.basic.._macro_.progn
        (lambda :
          (lambda * _: _)(
            (lambda * _: _)(
              'builtins..setattr',
              QzDOLR_fn,
              (lambda * _: _)(
                'quote',
                '__doc__'),
              docstring)))()),
      (lambda :())),qn=(lambda * _: _)(
      'builtins..setattr',
      QzDOLR_fn,
      (lambda * _: _)(
        'quote',
        '__qualname__'),
      (lambda * _: _)(
        '.join',
        "('.')",
        (lambda * _: _)(
          'quote',
          (lambda * _: _)(
            '_macro_',
            name)))):
      (lambda * _: _)(
        'hissp.basic.._macro_.let',
        (lambda * _: _)(
          QzDOLR_fn,
          fn),
        *ns,
        *dc,
        qn,
        (lambda * _: _)(
          'builtins..setattr',
          (lambda * _: _)(
            'operator..getitem',
            (lambda * _: _)(
              'builtins..globals'),
            (lambda * _: _)(
              'quote',
              '_macro_')),
          (lambda * _: _)(
            'quote',
            name),
          QzDOLR_fn)))())()):(
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__doc__',
    ('Creates a new macro for the current module.\n'
     '\n'
     "  If there's no ``_macro_``, creates one (using `types.ModuleType`).\n"
     "  If there's a docstring, stores it as the new lambda's ``__doc__``.\n"
     "  Adds the ``_macro_`` prefix to the lambda's ``__qualname__``.\n"
     '  Saves the lambda in ``_macro_`` using the given attribute name.\n'
     '  ')),
  __import__('builtins').setattr(
    _G_QzNo1_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'defmacro',))),
  __import__('builtins').setattr(
    __import__('builtins').globals()['_macro_'],
    'defmacro',
    _G_QzNo1_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda name,value:(
  ('Assigns a global the value in the current module.'),
  (lambda * _: _)(
    '.update',
    (lambda * _: _)(
      'builtins..globals'),
    ':',
    name,
    value))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Assigns a global the value in the current module.')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'define',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'define',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda name,bases,*body:(
  ('Defines a type (class) in the current module.\n'
   '\n'
   '  Key-value pairs are implied in the body.\n'
   '  '),
  (lambda * _: _)(
    'hissp.basic.._macro_.define',
    name,
    (lambda * _: _)(
      'builtins..type',
      (lambda * _: _)(
        'quote',
        name),
      (lambda * _: _)(
        __import__('hissp.reader',fromlist='?').ENTUPLE,
        *bases),
      (lambda * _: _)(
        'builtins..dict',
        ':',
        *body))))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Defines a type (class) in the current module.\n'
     '\n'
     '  Key-value pairs are implied in the body.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'deftype',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'deftype',
    _fn_QzNo7_))[-1])()

# define
__import__('builtins').globals().update(
  _TAO=('\n'
        'Abguvatarff nobir nofgenpgvba\n'
        '  ohg vzcyrzragngvba vf / gur orfg anzr.\n'
        'Grefrarff znl znxr bar gbb znal / trg hfrq gb gurz\n'
        '  ryfr biresybj lbhe oenva.\n'
        'Ab fhofgvghgr sbe haqrefgnaqvat\n'
        'Pbqr;     gur yvnovyvgl\n'
        'nf nffrg; gur   novyvgl.\n'
        'Gur ovttrfg puhaxf / ner uneq gb fjnyybj\n'
        '  nf fvzcyr nf cbffvoyr / ab zber.\n'
        'Fbhepr jnf znqr / sbe gur uhzna\n'
        '  bowrpg / gur znpuvar.\n'
        'Ner lbh ynml rabhtu gb orne / gur fvaprerfg sbez / bs bgure jnlf bs orvat?\n'
        '*univat* qrprag fgnaqneqf / vf zber vzcbegnag / guna rknpgyl jung gurl ner\n'
        'Cresrpgvba / vf rkcrafvir\n'
        '  zntvp / uvtuyl cevprq\n'
        "  cnl sbe jura / vg'f Jbegu Vg\n"
        '  n dhnegre vf nqivfrq\n'
        'Ernqnovyvgl / vf znvayl / ynvq bhg ba gur cntr.\n'
        'Tbysvat / znxrf tbbq cenpgvpr / orfg cenpgvpr vg orgenlf.\n'
        'Pnfgyrf ohvyg / va gur nve / juvgure gurl qb orybat?\n'
        '  Ryrtnapr / gura rkprcgvba\n'
        '  Sbez / orsber qrgnvy\n'
        '  jurapr haqre gurz,\n'
        'Sbhaqngvbaf nccrne.\n'
        'Znxr gur evtug jnl boivbhf,\n'
        'zrqvgngr ba guvf.\n'
        '  --Mn Mra bs Uvffc\n'))

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda target,*args:(
  ('Attaches the named variables to the target as attributes.\n'
   '\n'
   '  Positional arguments must be unqualified identifiers,\n'
   '  and use that as the attribute name.\n'
   '  Names after the ``:`` are identifier-value pairs.\n'
   '  Returns the target.\n'
   '  '),
  # let
  (lambda iargs=iter(
    args),QzDOLR_target='_target_QzNo15_':
    # let
    (lambda args=__import__('itertools').takewhile(
      (lambda a:
        __import__('operator').ne(
          a,
          ':')),
      iargs):
      (lambda * _: _)(
        'hissp.basic.._macro_.let',
        (lambda * _: _)(
          QzDOLR_target,
          target),
        *map(
           (lambda arg:
             (lambda * _: _)(
               'builtins..setattr',
               QzDOLR_target,
               (lambda * _: _)(
                 'quote',
                 arg),
               arg)),
           args),
        *map(
           (lambda kw:
             (lambda * _: _)(
               'builtins..setattr',
               QzDOLR_target,
               (lambda * _: _)(
                 'quote',
                 kw),
               next(
                 iargs))),
           iargs),
        QzDOLR_target))())())[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Attaches the named variables to the target as attributes.\n'
     '\n'
     '  Positional arguments must be unqualified identifiers,\n'
     '  and use that as the attribute name.\n'
     '  Names after the ``:`` are identifier-value pairs.\n'
     '  Returns the target.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'attach',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'attach',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda self,*invocations:(
  ('Configure an object.\n'
   '\n'
   "  Calls multiple 'methods' on one 'self'.\n"
   '\n'
   '  Evaluates the given ``self``, then injects it as the first argument to\n'
   '  a sequence of invocations. Returns ``self``.\n'
   '  '),
  # let
  (lambda QzDOLR_self='_self_QzNo19_':
    (lambda * _: _)(
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          QzDOLR_self,
          self),
        *map(
           (lambda invocation:
             (lambda * _: _)(
               __import__('operator').getitem(
                 invocation,
                 (0)),
               QzDOLR_self,
               *__import__('operator').getitem(
                  invocation,
                  slice(
                    (1),
                    None)))),
           invocations),
        QzDOLR_self)))())[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Configure an object.\n'
     '\n'
     "  Calls multiple 'methods' on one 'self'.\n"
     '\n'
     '  Evaluates the given ``self``, then injects it as the first argument to\n'
     '  a sequence of invocations. Returns ``self``.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'doto',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'doto',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda expr,*forms:(
  ("``->`` 'Thread-first'.\n"
   '\n'
   '  Converts a pipeline to function calls by recursively threading\n'
   '  expressions as the first argument of the next form.\n'
   '  E.g. ``(-> x (A b) (C d e))`` is ``(C (A x b) d e)``\n'
   '  Makes chained method calls easier to read.\n'
   '  '),
  # ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    forms,
    (lambda :
      (lambda * _: _)(
        'hissp.basic..QzMaybe_.Qz_QzGT_',
        (lambda * _: _)(
          __import__('operator').getitem(
            __import__('operator').getitem(
              forms,
              (0)),
            (0)),
          expr,
          *__import__('operator').getitem(
             __import__('operator').getitem(
               forms,
               (0)),
             slice(
               (1),
               None))),
        *__import__('operator').getitem(
           forms,
           slice(
             (1),
             None)))),
    (lambda :expr)))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ("``->`` 'Thread-first'.\n"
     '\n'
     '  Converts a pipeline to function calls by recursively threading\n'
     '  expressions as the first argument of the next form.\n'
     '  E.g. ``(-> x (A b) (C d e))`` is ``(C (A x b) d e)``\n'
     '  Makes chained method calls easier to read.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'Qz_QzGT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'Qz_QzGT_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda expr,*forms:(
  ("``->>`` 'Thread-last'.\n"
   '\n'
   '  Converts a pipeline to function calls by recursively threading\n'
   '  expressions as the last argument of the next form.\n'
   '  E.g. ``(->> x (A b) (C d e))`` is ``(C d e (A b x))``.\n'
   '  Can replace partial application in some cases.\n'
   '  Also works inside a ``->`` pipeline.\n'
   '  E.g. ``(-> x (A a) (->> B b) (C c))`` is ``(C (B b (A x a)) c)``.\n'
   '  '),
  # ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    forms,
    (lambda :
      (lambda * _: _)(
        'hissp.basic..QzMaybe_.Qz_QzGT_QzGT_',
        (lambda * _: _)(
          *__import__('operator').getitem(
             forms,
             (0)),
          expr),
        *__import__('operator').getitem(
           forms,
           slice(
             (1),
             None)))),
    (lambda :expr)))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ("``->>`` 'Thread-last'.\n"
     '\n'
     '  Converts a pipeline to function calls by recursively threading\n'
     '  expressions as the last argument of the next form.\n'
     '  E.g. ``(->> x (A b) (C d e))`` is ``(C d e (A b x))``.\n'
     '  Can replace partial application in some cases.\n'
     '  Also works inside a ``->`` pipeline.\n'
     '  E.g. ``(-> x (A a) (->> B b) (C c))`` is ``(C (B b (A x a)) c)``.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'Qz_QzGT_QzGT_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'Qz_QzGT_QzGT_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda *pairs:(
  ('Multiple condition branching.\n'
   '\n'
   '  Pairs are implied. Default is ``()``. Use ``:else`` to change it.\n'
   '  For example::\n'
   '\n'
   '   (cond) ; ()\n'
   "   ;; Assume some number 'x\n"
   '   (cond (operator..gt x 0) (print "positive")\n'
   '         (operator..lt x 0) (print "negative")\n'
   '         (operator..eq x 0) (print "zero")\n'
   '         :else (print "not a number"))\n'
   '  '),
  # when
  # hissp.basic.._macro_.ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    pairs,
    (lambda :
      # hissp.basic.._macro_.progn
      (lambda :
        (lambda * _: _)(
          'hissp.basic.._macro_.ifQz_else',
          __import__('operator').getitem(
            pairs,
            (0)),
          __import__('operator').getitem(
            pairs,
            (1)),
          (lambda * _: _)(
            'hissp.basic..QzMaybe_.cond',
            *__import__('operator').getitem(
               pairs,
               slice(
                 (2),
                 None)))))()),
    (lambda :())))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Multiple condition branching.\n'
     '\n'
     '  Pairs are implied. Default is ``()``. Use ``:else`` to change it.\n'
     '  For example::\n'
     '\n'
     '   (cond) ; ()\n'
     "   ;; Assume some number 'x\n"
     '   (cond (operator..gt x 0) (print "positive")\n'
     '         (operator..lt x 0) (print "negative")\n'
     '         (operator..eq x 0) (print "zero")\n'
     '         :else (print "not a number"))\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'cond',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'cond',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda variable,iterable,*body:(
  ('``any-for``\n'
   '  Bind the variable and evaluate the body for each item from the\n'
   '  iterable until any result is true (and return ``True``),\n'
   '  or until the iterable is exhausted (and return ``False``).\n'
   '  '),
  (lambda * _: _)(
    'builtins..any',
    (lambda * _: _)(
      'builtins..map',
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          variable),
        *body),
      iterable)))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('``any-for``\n'
     '  Bind the variable and evaluate the body for each item from the\n'
     '  iterable until any result is true (and return ``True``),\n'
     '  or until the iterable is exhausted (and return ``False``).\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'anyQz_for',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'anyQz_for',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda *exprs:(
  ("``&&`` 'and'. Shortcutting logical AND.\n"
   '  Returns the first false value, otherwise the last value.\n'
   '  There is an implicit initial value of ``True``.\n'
   '  '),
  # cond
  # hissp.basic.._macro_.ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    __import__('operator').not_(
      exprs),
    (lambda :True),
    (lambda :
      # hissp.basic..QzMaybe_.cond
      # hissp.basic.._macro_.ifQz_else
      (lambda test,*thenQz_else:
        __import__('operator').getitem(
          thenQz_else,
          __import__('operator').not_(
            test))())(
        __import__('operator').eq(
          len(
            exprs),
          (1)),
        (lambda :
          __import__('operator').getitem(
            exprs,
            (0))),
        (lambda :
          # hissp.basic..QzMaybe_.cond
          # hissp.basic.._macro_.ifQz_else
          (lambda test,*thenQz_else:
            __import__('operator').getitem(
              thenQz_else,
              __import__('operator').not_(
                test))())(
            ':else',
            (lambda :
              (lambda * _: _)(
                'hissp.basic.._macro_.let',
                (lambda * _: _)(
                  '_G_QzNo26_',
                  __import__('operator').getitem(
                    exprs,
                    (0))),
                (lambda * _: _)(
                  'hissp.basic.._macro_.ifQz_else',
                  '_G_QzNo26_',
                  (lambda * _: _)(
                    'hissp.basic..QzMaybe_.QzET_QzET_',
                    *__import__('operator').getitem(
                       exprs,
                       slice(
                         (1),
                         None))),
                  '_G_QzNo26_'))),
            (lambda :
              # hissp.basic..QzMaybe_.cond
              ())))))))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ("``&&`` 'and'. Shortcutting logical AND.\n"
     '  Returns the first false value, otherwise the last value.\n'
     '  There is an implicit initial value of ``True``.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzET_QzET_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzET_QzET_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda first=(),*rest:(
  ("``||`` 'or'. Shortcutting logical OR.\n"
   '  Returns the first true value, otherwise the last value.\n'
   '  There is an implicit initial value of ``()``.\n'
   '  '),
  # ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    rest,
    (lambda :
      (lambda * _: _)(
        'hissp.basic.._macro_.let',
        (lambda * _: _)(
          '_first_QzNo27_',
          first),
        (lambda * _: _)(
          'hissp.basic.._macro_.ifQz_else',
          '_first_QzNo27_',
          '_first_QzNo27_',
          (lambda * _: _)(
            'hissp.basic..QzMaybe_.QzBAR_QzBAR_',
            *rest)))),
    (lambda :first)))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ("``||`` 'or'. Shortcutting logical OR.\n"
     '  Returns the first true value, otherwise the last value.\n'
     '  There is an implicit initial value of ``()``.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzBAR_QzBAR_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzBAR_QzBAR_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda expr1,*body:(
  ('Evaluates each expression in sequence (for side effects),\n'
   '  resulting in the value of the first.'),
  (lambda * _: _)(
    'hissp.basic.._macro_.let',
    (lambda * _: _)(
      '_value1_QzNo28_',
      expr1),
    *body,
    '_value1_QzNo28_'))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Evaluates each expression in sequence (for side effects),\n'
     '  resulting in the value of the first.')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'prog1',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'prog1',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda raw:(
  ('``b#`` bytes literal reader macro'),
  # Qz_QzGT_
  # hissp.basic..QzMaybe_.Qz_QzGT_
  # hissp.basic..QzMaybe_.Qz_QzGT_
  # hissp.basic..QzMaybe_.Qz_QzGT_
  # hissp.basic..QzMaybe_.Qz_QzGT_
  # hissp.basic..QzMaybe_.Qz_QzGT_
  __import__('ast').literal_eval(
    # Qz_QzGT_QzGT_
    # hissp.basic..QzMaybe_.Qz_QzGT_QzGT_
    ("b'{}'").format(
      __import__('ast').literal_eval(
        raw).replace(
        ("'"),
        ("\\'")).replace(
        ('\n'),
        ('\\n')))))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('``b#`` bytes literal reader macro')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'bQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'bQzHASH_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda single,*lines:(
  ('``<<#`` comment-string reader macro.\n'
   '\n'
   '  Converts a line comment to a raw string.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> <<#;Don\'t worry about the "quotes".\n'
   '     >>> \'Don\'t worry about the "quotes".\'\n'
   '     \'Don\'t worry about the "quotes".\'\n'
   '\n'
   '  Or joins extra comments with a string object,\n'
   '  such as ``#"\\n"``.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> <<#\n'
   '     #..!;C:\\bin\n'
   '     #..!;C:\\Users\\ME\\Documents\n'
   '     #..!;C:\\Users\\ME\\Pictures\n'
   '     #..";"\n'
   '     >>> '
   "'C:\\\\bin;C:\\\\Users\\\\ME\\\\Documents;C:\\\\Users\\\\ME\\\\Pictures'\n"
   '     '
   "'C:\\\\bin;C:\\\\Users\\\\ME\\\\Documents;C:\\\\Users\\\\ME\\\\Pictures'\n"
   '\n'
   '  '),
  # ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    lines,
    (lambda :
      (lambda * _: _)(
        'quote',
        __import__('ast').literal_eval(
          single).join(
          map(
            __import__('operator').attrgetter(
              'content'),
            lines)))),
    (lambda :
      (lambda * _: _)(
        'quote',
        getattr(
          single,
          'content')))))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('``<<#`` comment-string reader macro.\n'
     '\n'
     '  Converts a line comment to a raw string.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> <<#;Don\'t worry about the "quotes".\n'
     '     >>> \'Don\'t worry about the "quotes".\'\n'
     '     \'Don\'t worry about the "quotes".\'\n'
     '\n'
     '  Or joins extra comments with a string object,\n'
     '  such as ``#"\\n"``.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> <<#\n'
     '     #..!;C:\\bin\n'
     '     #..!;C:\\Users\\ME\\Documents\n'
     '     #..!;C:\\Users\\ME\\Pictures\n'
     '     #..";"\n'
     '     >>> '
     "'C:\\\\bin;C:\\\\Users\\\\ME\\\\Documents;C:\\\\Users\\\\ME\\\\Pictures'\n"
     '     '
     "'C:\\\\bin;C:\\\\Users\\\\ME\\\\Documents;C:\\\\Users\\\\ME\\\\Pictures'\n"
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'QzLT_QzLT_QzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'QzLT_QzLT_QzHASH_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda f:(
  ('``en#`` reader macro.\n'
   '  Wrap a function of one iterable as a function of its elements.\n'
   '\n'
   '  .. code-block:: REPL\n'
   '\n'
   '     #> (en#list 1 2 3)\n'
   '     >>> (lambda *_xs_QzNo31_:\n'
   '     ...   list(\n'
   '     ...     _xs_QzNo31_))(\n'
   '     ...   (1),\n'
   '     ...   (2),\n'
   '     ...   (3))\n'
   '     [1, 2, 3]\n'
   '\n'
   '     #> (en#.extend _ 4 5 6) ; Methods too.\n'
   '     >>> (lambda _self_QzNo31_,*_xs_QzNo31_:\n'
   '     ...   _self_QzNo31_.extend(\n'
   '     ...     _xs_QzNo31_))(\n'
   '     ...   _,\n'
   '     ...   (4),\n'
   '     ...   (5),\n'
   '     ...   (6))\n'
   '\n'
   '     #> _\n'
   '     >>> _\n'
   '     [1, 2, 3, 4, 5, 6]\n'
   '\n'
   '  '),
  # ifQz_else
  (lambda test,*thenQz_else:
    __import__('operator').getitem(
      thenQz_else,
      __import__('operator').not_(
        test))())(
    # QzET_QzET_
    # hissp.basic.._macro_.let
    (lambda _G_QzNo26_=__import__('operator').is_(
      str,
      type(
        f)):
      # hissp.basic.._macro_.ifQz_else
      (lambda test,*thenQz_else:
        __import__('operator').getitem(
          thenQz_else,
          __import__('operator').not_(
            test))())(
        _G_QzNo26_,
        (lambda :
          # hissp.basic..QzMaybe_.QzET_QzET_
          f.startswith(
            ('.'))),
        (lambda :_G_QzNo26_)))(),
    (lambda :
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          '_self_QzNo31_',
          ':',
          ':*',
          '_xs_QzNo31_'),
        (lambda * _: _)(
          f,
          '_self_QzNo31_',
          '_xs_QzNo31_'))),
    (lambda :
      (lambda * _: _)(
        'lambda',
        (lambda * _: _)(
          ':',
          ':*',
          '_xs_QzNo32_'),
        (lambda * _: _)(
          f,
          '_xs_QzNo32_')))))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('``en#`` reader macro.\n'
     '  Wrap a function of one iterable as a function of its elements.\n'
     '\n'
     '  .. code-block:: REPL\n'
     '\n'
     '     #> (en#list 1 2 3)\n'
     '     >>> (lambda *_xs_QzNo31_:\n'
     '     ...   list(\n'
     '     ...     _xs_QzNo31_))(\n'
     '     ...   (1),\n'
     '     ...   (2),\n'
     '     ...   (3))\n'
     '     [1, 2, 3]\n'
     '\n'
     '     #> (en#.extend _ 4 5 6) ; Methods too.\n'
     '     >>> (lambda _self_QzNo31_,*_xs_QzNo31_:\n'
     '     ...   _self_QzNo31_.extend(\n'
     '     ...     _xs_QzNo31_))(\n'
     '     ...   _,\n'
     '     ...   (4),\n'
     '     ...   (5),\n'
     '     ...   (6))\n'
     '\n'
     '     #> _\n'
     '     >>> _\n'
     '     [1, 2, 3, 4, 5, 6]\n'
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'enQzHASH_',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'enQzHASH_',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda ns=(lambda * _: _)(
  'builtins..globals'):(
  ('The basic prelude.\n'
   '\n'
   '  Imports `functools.partial` and `functools.reduce`.\n'
   '  Star imports from `itertools` and `operator`.\n'
   '  Defines the en- group: ``entuple``, ``enlist``, ``enset``, ``endict``,\n'
   '  and ``enstr``, which build collections from individual elements,\n'
   '  and ``engarde``, which calls a function for you, handling any targeted\n'
   '  exception with the given handler.\n'
   '\n'
   '  Adds the basic macros, but only if available,\n'
   '  so its expansion does not require Hissp to be installed.\n'
   '  (This replaces ``_macro_`` if you already had one.)\n'
   '\n'
   "  Mainly intended for single-file scripts that can't have dependencies,\n"
   '  or similarly constrained environments (e.g. embedded, readerless).\n'
   '  There, the first form should be ``(hissp.basic.._macro_.prelude)``,\n'
   '  which is also implied in ``$ lissp -c`` commands.\n'
   '\n'
   '  Larger projects with access to functional and macro libraries need not\n'
   '  use this prelude at all.\n'
   '\n'
   '  The REPL has the basic macros loaded by default, but not the prelude.\n'
   '  Invoke ``(prelude)`` to get the rest.\n'
   '  '),
  (lambda * _: _)(
    'builtins..exec',
    (lambda * _: _)(
      'quote',
      ('from functools import partial,reduce\n'
       'from itertools import *;from operator import *\n'
       'def entuple(*xs):return xs\n'
       'def enlist(*xs):return[*xs]\n'
       'def enset(*xs):return{{*xs}}\n'
       "def enfrost(*xs):return __import__('builtins').frozenset(xs)\n"
       'def endict(*kvs):return{{k:i.__next__()for i in[kvs.__iter__()]for k in i}}\n'
       "def enstr(*xs):return''.join(''.__class__(x)for x in xs)\n"
       'def engarde(xs,h,f,/,*a,**kw):\n'
       ' try:return f(*a,**kw)\n'
       ' except xs as e:return h(e)\n'
       "_macro_=__import__('types').SimpleNamespace()\n"
       "try:exec('from {}._macro_ import *',vars(_macro_))\n"
       'except ModuleNotFoundError:pass').format(
        __name__)),
    ns))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('The basic prelude.\n'
     '\n'
     '  Imports `functools.partial` and `functools.reduce`.\n'
     '  Star imports from `itertools` and `operator`.\n'
     '  Defines the en- group: ``entuple``, ``enlist``, ``enset``, ``endict``,\n'
     '  and ``enstr``, which build collections from individual elements,\n'
     '  and ``engarde``, which calls a function for you, handling any targeted\n'
     '  exception with the given handler.\n'
     '\n'
     '  Adds the basic macros, but only if available,\n'
     '  so its expansion does not require Hissp to be installed.\n'
     '  (This replaces ``_macro_`` if you already had one.)\n'
     '\n'
     "  Mainly intended for single-file scripts that can't have dependencies,\n"
     '  or similarly constrained environments (e.g. embedded, readerless).\n'
     '  There, the first form should be ``(hissp.basic.._macro_.prelude)``,\n'
     '  which is also implied in ``$ lissp -c`` commands.\n'
     '\n'
     '  Larger projects with access to functional and macro libraries need not\n'
     '  use this prelude at all.\n'
     '\n'
     '  The REPL has the basic macros loaded by default, but not the prelude.\n'
     '  Invoke ``(prelude)`` to get the rest.\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'prelude',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'prelude',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda *args:
  (lambda * _: _)(
    'builtins..print',
    (lambda * _: _)(
      'codecs..encode',
      'hissp.basic.._TAO',
      (lambda * _: _)(
        'quote',
        'rot13')))):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'import',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'import',
    _fn_QzNo7_))[-1])()

# defmacro
# hissp.basic.._macro_.let
(lambda _fn_QzNo7_=(lambda alias,module:(
  ('Defines a reader macro abbreviation of a qualifier. For example,\n'
   '\n'
   '  .. code-block:: Lissp\n'
   '\n'
   '     (hissp.basic.._macro_.alias M/ hissp.basic.._macro_)\n'
   '     ;; Now the same as (hissp.basic.._macro_.alias op sub.).\n'
   '     (M/#alias op operator.)\n'
   '     ;; Use an extra to name a reader macro.\n'
   '     M/#!b"byte string"\n'
   '     (op#sub 2 3)\n'
   '     #> op#!pow !3 2\n'
   '     >>> (8)\n'
   '     8\n'
   '\n'
   '  '),
  (lambda * _: _)(
    'hissp.basic.._macro_.defmacro',
    ('{}{}').format(
      alias,
      'QzHASH_'),
    (lambda * _: _)(
      '_prime_QzNo36_',
      ':',
      '_reader_QzNo36_',
      None,
      ':*',
      '_args_QzNo36_'),
    (lambda * _: _)(
      'quote',
      ("('Aliases {} as {}#')").format(
        module,
        alias)),
    (lambda * _: _)(
      'hissp.basic.._macro_.ifQz_else',
      '_reader_QzNo36_',
      (lambda * _: _)(
        (lambda * _: _)(
          'builtins..getattr',
          module,
          (lambda * _: _)(
            '.format',
            "('{}{}')",
            '_reader_QzNo36_',
            (lambda * _: _)(
              'hissp.basic.._macro_.ifQz_else',
              (lambda * _: _)(
                'operator..contains',
                (lambda * _: _)(
                  'quote',
                  module),
                (lambda * _: _)(
                  'quote',
                  '_macro_')),
              (lambda * _: _)(
                'quote',
                'QzHASH_'),
              "('')"))),
        '_prime_QzNo36_',
        ':',
        ':*',
        '_args_QzNo36_'),
      (lambda * _: _)(
        '.format',
        "('{}.{}')",
        (lambda * _: _)(
          'quote',
          module),
        '_prime_QzNo36_'))))[-1]):(
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__doc__',
    ('Defines a reader macro abbreviation of a qualifier. For example,\n'
     '\n'
     '  .. code-block:: Lissp\n'
     '\n'
     '     (hissp.basic.._macro_.alias M/ hissp.basic.._macro_)\n'
     '     ;; Now the same as (hissp.basic.._macro_.alias op sub.).\n'
     '     (M/#alias op operator.)\n'
     '     ;; Use an extra to name a reader macro.\n'
     '     M/#!b"byte string"\n'
     '     (op#sub 2 3)\n'
     '     #> op#!pow !3 2\n'
     '     >>> (8)\n'
     '     8\n'
     '\n'
     '  ')),
  __import__('builtins').setattr(
    _fn_QzNo7_,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'alias',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'alias',
    _fn_QzNo7_))[-1])()