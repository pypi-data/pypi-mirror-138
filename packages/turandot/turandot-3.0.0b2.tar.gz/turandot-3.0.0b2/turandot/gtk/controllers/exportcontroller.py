import multiprocessing
from typing import Optional
from pathlib import Path
from turandot import TurandotAssetException
from turandot.model import ConversionAlgorithm, ReferenceSource, JobSettings, ConversionJob, JobAssets, ConversionProcessor, ConverterChain, SourceAsset
from turandot.ui import catch_exception, FrontendUtils
from turandot.gtk import TurandotGtkView
from turandot.gtk.controllers import BaseController, GtkConversionUpdater


class ExportController(BaseController):
    """Controller to handle buttons related to the conversion process"""

    def __init__(self, view: TurandotGtkView):
        self.msgqueue = multiprocessing.Queue()
        self.processor: Optional[ConversionProcessor] = None
        self.last_open_folder_id: Optional[int] = None
        BaseController.__init__(self, view)

    def connect_events(self):
        self.view.get_element("export_launch_button").connect("clicked", self._launch_conversion)
        self.view.get_element("export_cancel_button").connect("clicked", self._cancel_conversion)

    def _collect_job_settings(self) -> JobSettings:
        """Collect settings for conversion job from GUI"""
        convalg: ConversionAlgorithm = self.view.get_element("conversion_algorithm_dropdown").get_selected_value()
        refsrc: ReferenceSource = self.view.get_element("reference_source_dropdown").get_selected_value()
        if refsrc == ReferenceSource.ZOTERO:
            zotlib: Optional[int] = int(self.view.get_element("zotero_lib_dropdown").get_active_id())
        else:
            zotlib = None
        return JobSettings(convalg, refsrc, zotlib)

    @catch_exception
    def _collect_job(self) -> Optional[ConversionJob]:
        """Collect settings and assets for conversion job from GUI"""
        settings = self._collect_job_settings()
        srcstring = self.view.get_element("source_file_entry").get_text()
        if srcstring == "":
            raise TurandotAssetException('Field "Source file" must not be empty')
        srcasset = SourceAsset(path=Path(self.view.get_element("source_file_entry").get_text()), expand=True)
        tmplasset = self.view.get_element("template_dropdown").get_selected_asset()
        if settings.reference_source.value > 1:
            cslasset = self.view.get_element("csl_dropdown").get_selected_asset()
        else:
            cslasset = None
        if settings.reference_source == ReferenceSource.JSON:
            csljson = self.view.get_element("csljson_file_entry").get_text()
            if csljson == "":
                raise TurandotAssetException('Field "CSLJSON file" must not be empty')
        else:
            csljson = None
        assets = JobAssets(srcasset, tmplasset, cslasset, csljson)
        return ConversionJob(assets, settings, self.msgqueue)

    def _create_processor(self) -> Optional[ConversionProcessor]:
        """Create converter object"""
        job = self._collect_job()
        if job is None:
            return None
        chain = ConverterChain.build_chain(job.job_settings.conversion_algorithm)
        frontendstrat = GtkConversionUpdater(self.view)
        return ConversionProcessor(job, chain, frontendstrat)

    def _reattach_open_folder_callback(self, path: Path):
        """Attach correct path to callback on 'Open Folder' button"""
        if self.last_open_folder_id is not None:
            self.view.get_element("open_result_folder").disconnect(self.last_open_folder_id)
        self.last_open_folder_id = self.view.get_element("open_result_folder").connect("clicked", FrontendUtils.fm_open_path, path)

    def _launch_conversion(self, *args):
        """Launch conversion process"""
        self.processor = self._create_processor()
        if self.processor is None:
            return None
        self._reattach_open_folder_callback(self.processor.conversionjob.job_assets.sourcefile.directory)
        self.processor.start_conversion()

    def _cancel_conversion(self, *args):
        """Kill conversion process prematurely"""
        self.processor.kill_conversion()
