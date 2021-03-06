"""Handle generation and management of latex variable files."""


def write_tex_vars(tex_vars):
    """Convert a dictionary to a tex variable file."""
    if not isinstance(tex_vars, dict):
        raise TypeError('tex_vars must be a dictionary')

    var_file = open('.working/vars.tex', 'w')

    for key in tex_vars:
        if isinstance(tex_vars[key], str) and tex_vars[key][-4:] == '.png':
            var_file.write("\\newcommand{\%s}{%s}\n" % (key, tex_vars[key]))
        else:
            var_file.write("\\newcommand{\%s}{%s }\n" % (key, tex_vars[key]))

    var_file.close()
