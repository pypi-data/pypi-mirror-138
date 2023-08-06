"use strict";
(self["webpackChunkjupyterlab_autoimport"] = self["webpackChunkjupyterlab_autoimport"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);





const plugin = {
    id: "@jupyterlab/autoimport:plugin",
    autoStart: true,
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        app.commands.addCommand("refresh-imports", {
            label: "Refresh Imports",
            execute: () => {
                const current = notebookTracker === null || notebookTracker === void 0 ? void 0 : notebookTracker.currentWidget;
                const notebook = current === null || current === void 0 ? void 0 : current.content;
                if (!current || current !== app.shell.currentWidget ||
                    !(notebook === null || notebook === void 0 ? void 0 : notebook.model) || !notebook.activeCell) {
                    return;
                }
                const outputArea = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.SimplifiedOutputArea({
                    model: new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputAreaModel(),
                    rendermime: current.content.rendermime,
                });
                const printImports = `
          if '_imported' not in dir(get_ipython().user_ns):
            %load_ext ipython_autoimport
          print(*get_ipython().user_ns._imported, sep='\\n')
        `;
                _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.SimplifiedOutputArea.execute(printImports, outputArea, current.sessionContext)
                    .then((msg) => {
                    var _a, _b;
                    if ((msg === null || msg === void 0 ? void 0 : msg.content.status) !== "ok") {
                        if ((msg === null || msg === void 0 ? void 0 : msg.content.status) === "error") {
                            alert(`${msg.content.ename}\n${msg.content.evalue}`);
                        }
                        else if (msg) {
                            alert(msg.content.status);
                        }
                        else {
                            alert("Unknown problem");
                        }
                        return;
                    }
                    const imports = outputArea.model.toJSON().map(output => output.text).join("");
                    var importsText = (imports != null) ? imports.replace(/\n+$/, "") : "";
                    notebook.activeCellIndex = 0;
                    const firstCodeCellIndex = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.findIndex)(((_a = notebook.model) === null || _a === void 0 ? void 0 : _a.cells) || [], (cell, index) => (0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.isCodeCellModel)(cell));
                    if (firstCodeCellIndex !== -1) {
                        notebook.activeCellIndex = firstCodeCellIndex;
                    }
                    notebook.deselectAll();
                    if (notebook.activeCell === null || !(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.isCodeCellModel)(notebook.activeCell.model)) {
                        return;
                    }
                    _lumino_domutils__WEBPACK_IMPORTED_MODULE_3__.ElementExt.scrollIntoViewIfNeeded(notebook.node, notebook.activeCell.node);
                    const cellText = notebook.activeCell.model.value.text;
                    const start = (_b = cellText.match(/^(import|from) /m)) === null || _b === void 0 ? void 0 : _b.index;
                    const end = (start != null) ? cellText.indexOf("\n\n", start) : null;
                    var before, after;
                    if (start != null && end != null) {
                        before = cellText.slice(0, start);
                        after = ((end >= 0) ? cellText.slice(end) : "");
                    }
                    else {
                        before = "";
                        after = cellText;
                    }
                    after = after.replace(/^\n+/, "");
                    if (importsText !== "" && after !== "") {
                        importsText = importsText + "\n\n";
                    }
                    notebook.activeCell.model.value.text = before + importsText + after;
                });
            }
        });
        app.commands.addKeyBinding({
            command: "refresh-imports",
            keys: ["Accel K"],
            selector: ".jp-Notebook",
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.35f95420160244624313.js.map