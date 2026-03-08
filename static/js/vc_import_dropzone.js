(function (global) {
  'use strict';

  function formatFileSize(bytes) {
    if (!bytes || bytes === 0) return '0 Bytes';
    var k = 1024;
    var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    var value = Math.round((bytes / Math.pow(k, i)) * 100) / 100;
    return value + ' ' + sizes[i];
  }

  function init(options) {
    if (!options) return;

    var dropZone = document.getElementById(options.dropZoneId);
    var fileInput = document.getElementById(options.fileInputId);

    if (!dropZone || !fileInput) return;

    var dropZoneContent = options.dropZoneContentSelector
      ? dropZone.querySelector(options.dropZoneContentSelector)
      : null;

    var dropZoneFileInfo = options.dropZoneFileInfoSelector
      ? dropZone.querySelector(options.dropZoneFileInfoSelector)
      : null;

    var fileNameEl = options.fileNameId ? document.getElementById(options.fileNameId) : null;
    var fileSizeEl = options.fileSizeId ? document.getElementById(options.fileSizeId) : null;

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(function (eventName) {
      dropZone.addEventListener(eventName, preventDefaults, false);
      document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(function (eventName) {
      dropZone.addEventListener(
        eventName,
        function () {
          dropZone.classList.add('drag-over');
        },
        false
      );
    });

    ['dragleave', 'drop'].forEach(function (eventName) {
      dropZone.addEventListener(
        eventName,
        function () {
          dropZone.classList.remove('drag-over');
        },
        false
      );
    });

    function showFileInfo(file) {
      if (!file) return;

      if (fileNameEl) fileNameEl.textContent = file.name;
      if (fileSizeEl) fileSizeEl.textContent = formatFileSize(file.size);

      if (dropZoneContent) dropZoneContent.classList.add('d-none');
      if (dropZoneFileInfo) dropZoneFileInfo.classList.remove('d-none');

      if (typeof options.onFileSelected === 'function') {
        options.onFileSelected(file);
      }
    }

    dropZone.addEventListener(
      'drop',
      function (e) {
        var dt = e.dataTransfer;
        var files = dt && dt.files ? dt.files : null;

        if (files && files.length > 0) {
          try {
            fileInput.files = files;
          } catch (err) {
            // Em alguns navegadores, FileList pode ser somente leitura.
            // Mantemos apenas a visualização do arquivo selecionado.
          }
          showFileInfo(files[0]);
        }
      },
      false
    );

    fileInput.addEventListener(
      'change',
      function (e) {
        var files = e.target && e.target.files ? e.target.files : null;
        if (files && files.length > 0) {
          showFileInfo(files[0]);
        }
      },
      false
    );

    if (options.removeFileGlobalName) {
      global[options.removeFileGlobalName] = function () {
        try {
          fileInput.value = '';
        } catch (err) {
          // ignore
        }

        if (dropZoneContent) dropZoneContent.classList.remove('d-none');
        if (dropZoneFileInfo) dropZoneFileInfo.classList.add('d-none');

        if (typeof options.onFileRemoved === 'function') {
          options.onFileRemoved();
        }
      };
    }
  }

  global.VCImportDropZone = {
    init: init,
  };
})(window);
