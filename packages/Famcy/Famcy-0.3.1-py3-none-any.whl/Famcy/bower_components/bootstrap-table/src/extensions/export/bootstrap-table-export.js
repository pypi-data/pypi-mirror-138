/**
 * @author zhixin wen <wenzhixin2010@gmail.com>
 * extensions: https://github.com/hhurz/tableExport.jquery.plugin
 */

const Utils = $.fn.bootstrapTable.utils

const TYPE_NAME = {
  json: 'JSON',
  xml: 'XML',
  png: 'PNG',
  csv: 'CSV',
  txt: 'TXT',
  sql: 'SQL',
  doc: 'MS-Word',
  excel: 'MS-Excel',
  xlsx: 'MS-Excel (OpenXML)',
  powerpoint: 'MS-Powerpoint',
  pdf: 'PDF'
}

$.extend($.fn.bootstrapTable.defaults, {
  showExport: false,
  exportDataType: 'basic', // basic, all, selected
  exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel'],
  exportOptions: {
    onCellHtmlData (cell, rowIndex, colIndex, htmlData) {
      if (cell.is('th')) {
        return cell.find('.th-inner').text()
      }

      return htmlData
    }
  },
  exportFooter: false
})

$.extend($.fn.bootstrapTable.columnDefaults, {
  forceExport: false,
  forceHide: false
})

$.extend($.fn.bootstrapTable.defaults.icons, {
  export: {
    bootstrap3: 'glyphicon-export icon-share',
    materialize: 'file_download',
    'bootstrap-table': 'icon-download'
  }[$.fn.bootstrapTable.theme] || 'fa-download'
})

$.extend($.fn.bootstrapTable.locales, {
  formatExport () {
    return 'Export data'
  }
})
$.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales)

$.fn.bootstrapTable.methods.push('exportTable')

$.extend($.fn.bootstrapTable.defaults, {
  // eslint-disable-next-line no-unused-vars
  onExportSaved (exportedRows) {
    return false
  }
})

$.extend($.fn.bootstrapTable.Constructor.EVENTS, {
  'export-saved.bs.table': 'onExportSaved'
})

$.BootstrapTable = class extends $.BootstrapTable {
  initToolbar (...args) {
    const o = this.options
    let exportTypes = o.exportTypes

    this.showToolbar = this.showToolbar || o.showExport

    if (this.options.showExport) {

      if (typeof exportTypes === 'string') {
        const types = exportTypes.slice(1, -1).replace(/ /g, '').split(',')

        exportTypes = types.map(t => t.slice(1, -1))
      }

      this.$export = this.$toolbar.find('>.columns div.export')
      if (this.$export.length) {
        this.updateExportButton()
        return
      }

      this.buttons = Object.assign(this.buttons, {
        export: {
          html: exportTypes.length === 1 ? `
            <div class="export ${this.constants.classes.buttonsDropdown}"
            data-type="${exportTypes[0]}">
            <button class="${this.constants.buttonsClass}"
            aria-label="Export"
            type="button"
            title="${o.formatExport()}">
            ${o.showButtonIcons ? Utils.sprintf(this.constants.html.icon, o.iconsPrefix, o.icons.export) : ''}
            ${o.showButtonText ? o.formatExport() : ''}
            </button>
            </div>
          ` : `
            <div class="export ${this.constants.classes.buttonsDropdown}">
            <button class="${this.constants.buttonsClass} dropdown-toggle"
            aria-label="Export"
            ${this.constants.dataToggle}="dropdown"
            type="button"
            title="${o.formatExport()}">
            ${o.showButtonIcons ? Utils.sprintf(this.constants.html.icon, o.iconsPrefix, o.icons.export) : ''}
            ${o.showButtonText ? o.formatExport() : ''}
            ${this.constants.html.dropdownCaret}
            </button>
            </div>
          `
        }
      })
    }

    super.initToolbar(...args)
    this.$export = this.$toolbar.find('>.columns div.export')

    if (!this.options.showExport) {
      return
    }

    let $menu = $(this.constants.html.toolbarDropdown.join(''))
    let $items = this.$export

    if (exportTypes.length > 1) {
      this.$export.append($menu)

      // themes support
      if ($menu.children().length) {
        $menu = $menu.children().eq(0)
      }
      for (const type of exportTypes) {
        if (TYPE_NAME.hasOwnProperty(type)) {
          const $item = $(Utils.sprintf(this.constants.html.pageDropdownItem,
            '', TYPE_NAME[type]))

          $item.attr('data-type', type)
          $menu.append($item)
        }
      }

      $items = $menu.children()
    }

    this.updateExportButton()

    $items.click(e => {
      e.preventDefault()

      const type = $(e.currentTarget).data('type')
      const exportOptions = {
        type,
        escape: false
      }

      this.exportTable(exportOptions)
    })
    this.handleToolbar()
  }

  handleToolbar () {
    if (!this.$export) {
      return
    }

    if (super.handleToolbar) {
      super.handleToolbar()
    }
  }

  exportTable (options) {
    const o = this.options
    const stateField = this.header.stateField
    const isCardView = o.cardView

    const doExport = callback => {
      if (stateField) {
        this.hideColumn(stateField)
      }
      if (isCardView) {
        this.toggleView()
      }

      this.columns.forEach(row => {
        if (row.forceHide) {
          this.hideColumn(row.field)
        }
      })

      const data = this.getData()

      if (o.detailView && o.detailViewIcon) {
        const detailViewIndex = o.detailViewAlign === 'left' ? 0 : this.getVisibleFields().length + Utils.getDetailViewIndexOffset(this.options)

        o.exportOptions.ignoreColumn = [detailViewIndex].concat(o.exportOptions.ignoreColumn || [])
      }

      if (o.exportFooter) {
        const $footerRow = this.$tableFooter.find('tr').first()
        const footerData = {}
        const footerHtml = []

        $.each($footerRow.children(), (index, footerCell) => {
          const footerCellHtml = $(footerCell).children('.th-inner').first().html()

          footerData[this.columns[index].field] = footerCellHtml === '&nbsp;' ? null : footerCellHtml

          // grab footer cell text into cell index-based array
          footerHtml.push(footerCellHtml)
        })

        this.$body.append(this.$body.children().last()[0].outerHTML)
        const $lastTableRow = this.$body.children().last()

        $.each($lastTableRow.children(), (index, lastTableRowCell) => {
          $(lastTableRowCell).html(footerHtml[index])
        })
      }

      const hiddenColumns = this.getHiddenColumns()

      hiddenColumns.forEach(row => {
        if (row.forceExport) {
          this.showColumn(row.field)
        }
      })

      if (typeof o.exportOptions.fileName === 'function') {
        options.fileName = o.exportOptions.fileName()
      }

      this.$el.tableExport($.extend({
        onAfterSaveToFile: () => {
          if (o.exportFooter) {
            this.load(data)
          }

          if (stateField) {
            this.showColumn(stateField)
          }
          if (isCardView) {
            this.toggleView()
          }

          hiddenColumns.forEach(row => {
            if (row.forceExport) {
              this.hideColumn(row.field)
            }
          })

          this.columns.forEach(row => {
            if (row.forceHide) {
              this.showColumn(row.field)
            }
          })

          if (callback) callback()
        }
      }, o.exportOptions, options))
    }

    if (o.exportDataType === 'all' && o.pagination) {
      const eventName = o.sidePagination === 'server' ?
        'post-body.bs.table' : 'page-change.bs.table'
      const virtualScroll = this.options.virtualScroll

      this.$el.one(eventName, () => {
        setTimeout(() => {
          doExport(() => {
            this.options.virtualScroll = virtualScroll
            this.togglePagination()
          })
        }, 0)
      })
      this.options.virtualScroll = false
      this.togglePagination()
      this.trigger('export-saved', this.getData())
    } else if (o.exportDataType === 'selected') {
      let data = this.getData()
      let selectedData = this.getSelections()
      const pagination = o.pagination

      if (!selectedData.length) {
        return
      }

      if (o.sidePagination === 'server') {
        data = {
          total: o.totalRows,
          [this.options.dataField]: data
        }
        selectedData = {
          total: selectedData.length,
          [this.options.dataField]: selectedData
        }
      }

      this.load(selectedData)
      if (pagination) {
        this.togglePagination()
      }
      doExport(() => {
        if (pagination) {
          this.togglePagination()
        }
        this.load(data)
      })
      this.trigger('export-saved', selectedData)
    } else {
      doExport()
      this.trigger('export-saved', this.getData(true))
    }
  }

  updateSelected () {
    super.updateSelected()
    this.updateExportButton()
  }

  updateExportButton () {
    if (this.options.exportDataType === 'selected') {
      this.$export.find('> button')
        .prop('disabled', !this.getSelections().length)
    }
  }
}
