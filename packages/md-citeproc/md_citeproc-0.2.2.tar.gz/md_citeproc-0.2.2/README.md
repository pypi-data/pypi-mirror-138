# md_citeproc

_This package is in Alpha. While I'm trying to avoid it, the API might be subject to change._

Full Documentation: [Readthedocs](https://md-citeproc.readthedocs.io)

Python Markdown extension to render citeproc-style references and citations in Markdown documents. This extension aims to be highly configurable to accommodate a wide variety of use cases, notation styles and bibliographic conventions.

## Features

- Render citations based on a CSL style sheet and bibliographic data in CSLJSON
- Adapt to different notation styles and output styles
- Optionally, adjust rendering details by using [Jinja templates](https://jinja.palletsprojects.com/)
- Render footnotes and bibliographies
- Add uncited items to the bibliography on rendering

## Architecture

Under the hood, this extension uses the Nodejs package [`citeproc-cli`](https://www.npmjs.com/package/citeproc-cli) for the rendering process, which itself is based on [`citeproc-js`](https://www.npmjs.com/package/citeproc).

While this architecture limits the portability of the extension, it seems necessary to offer a feature-complete citeproc rendering process. To make things a little easier for a lot of users, [`pkg`](https://www.npmjs.com/package/pkg)-packaged executables for the operating system families Windows, MacOS and Linux on the amd64 platform are shiped with the extension. On these platforms, the extension can run without nodejs or additional configuration. On other platforms, either a [`citeproc-cli`](https://www.npmjs.com/package/citeproc-cli) installation or a [`pkg`](https://www.npmjs.com/package/pkg)-packaged executable of [`citeproc-cli`](https://www.npmjs.com/package/citeproc-cli) for the target platform is necessary to use the extension, the latter can be specified in the configuration of the extension.

## Links

- [Documentation](https://md-citeproc.readthedocs.io)
- [Source Code](https://gitlab.com/dinuthehuman/md_citeproc)
- [Issue Tracker](https://gitlab.com/dinuthehuman/md_citeproc/-/issues)
- [citeproc-cli@npm](https://www.npmjs.com/package/citeproc-cli)
