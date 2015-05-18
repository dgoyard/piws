#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cubicweb import
from cubicweb.predicates import is_instance
from cubicweb.view import EntityView

# Cubes import
from cubes.brainomics.views.outofcontext import ScanOutOfContextView
from cubes.brainomics.views.outofcontext import AssessmentOutOfContextView
from cubes.brainomics.views.outofcontext import QuestionnaireRunOutOfContextView
from cubes.brainomics.views.outofcontext import SubjectOutOfContextView

# PIWS import
from components import AUTHORIZED_IMAGE_EXT


###############################################################################
# Scans
###############################################################################

class NSScanOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("Scan")

    def cell_call(self, row, col):
        """ Create the NSScanOutOfContextView view line by line
        """
        # Get the scan entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the associated resources
        efentries = entity.results_files[0].file_entries
        imagefiles = [e.filepath for e in efentries
                     if e.filepath.endswith(tuple(AUTHORIZED_IMAGE_EXT))]
        limagefiles = len(imagefiles)
        if limagefiles > 0:
            href = self._cw.build_url(
                "view", vid="brainbrowser-image-viewer", imagefiles=imagefiles,
                __message=(u"Found '{0}' image(s) that can be "
                            "displayed.".format(limagefiles)))

        # Get the associated documentation if available
        tooltip = self._cw.vreg.docmap.get(entity.label, None)

        # Get the subject/study related entities
        subject = entity.subject[0]
        study = entity.study[0]

        # Get the scan image url
        image = u'<img alt="" src="%s">' % self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Type <em>{0}</em> - Fromat <em>{1}</em></div>'.format(entity.type, entity.format))
        # > third element: the see more button
        self.w(u'<button class="btn btn-danger" type="button" '
                'style="margin-top:8px" data-toggle="collapse" '
                'data-target="#info-{0}">'.format(row))
        self.w(u'See more')
        self.w(u'</button>')
        # > fourth element: the show button
        if limagefiles > 0:
            self.w(u'<a href="{0}" target=_blank class="btn btn-success" type="button" '
                    'style="margin-top:8px">'.format(href))
            self.w(u'Show &#9735')
            self.w(u'</a>')
        # > fifth element: the doc button
        if tooltip is not None:
            tiphref = self._cw.build_url("view", vid="piws-documentation",
                                         tooltip=tooltip, _notemplate=True)
            self.w(u'<button href="{0}" class="btn btn-warning" type="button" '
                    'style="margin-top:8px" data-toggle="collapse" '
                    'data-target="#doc-{0}">'.format(row))
            self.w(u'Doc')
            self.w(u'</button>')
            self.w(u'<a href="{0}" target=_blank class="btn btn-warning" type="button" '
                    'style="margin-top:8px">'.format(tiphref))
            self.w(u'&#9735')
            self.w(u'</a>')

        # Close row item
        self.w(u'</div>')

        # Get the scan description
        dtype_entity = entity.has_data[0]

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-{0}" class="collapse">'.format(row))
        self.w(u'<dl class="dl-horizontal">')
        # > image shape
        self.w(u'<dt>Image Shape (x)</dt><dd>{0}</dd>'.format(
            dtype_entity.shape_x))
        self.w(u'<dt>Image Shape (y)</dt><dd>{0}</dd>'.format(
            dtype_entity.shape_y))
        self.w(u'<dt>Image Shape (z)</dt><dd>{0}</dd>'.format(
            dtype_entity.shape_z))
        # > image resolution
        self.w(u'<dt>Voxel resolution (x)</dt><dd>{0}</dd>'.format(
            dtype_entity.voxel_res_x))
        self.w(u'<dt>Voxel resolution (y)</dt><dd>{0}</dd>'.format(
            dtype_entity.voxel_res_y))
        self.w(u'<dt>Voxel resolution (z)</dt><dd>{0}</dd>'.format(
            dtype_entity.voxel_res_z))
        # > image TR
        self.w(u'<dt>Repetition time</dt><dd>{0}</dd>'.format(
            dtype_entity.tr))
        # > image TE
        self.w(u'<dt>Echo time</dt><dd>{0}</dd>'.format(
            dtype_entity.te))
        # > Scanner field
        self.w(u'<dt>Scanner field</dt><dd>{0}</dd>'.format(
            dtype_entity.field))
        # > Realted entities
        self.w(u'<dt>Ralated subject</dt><dd>{0}</dd>'.format(
            subject.view("incontext")))
        self.w(u'<dt>Ralated study</dt><dd>{0}</dd>'.format(
            study.view("incontext")))
        self.w(u'</div>')

        # Create a div that will be show or hide when the doc button is
        # clicked
        self.w(u'<div id="doc-{0}" class="collapse">'.format(row))
        self.w(unicode(tooltip))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# Assessment
###############################################################################

class NSAssessmentOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("Assessment")

    def cell_call(self, row, col):
        """ Create the NSAssessmentOutOfContextView view line by line
        """
        # Get the assessment entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        related_subjects = entity.subjects
        study = entity.study[0]
        center = entity.center[0]
        run_items = []
        run_items.extend(entity.related_processing)
        run_items.extend(entity.uses)

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' % self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Study <em>{0}</em> - Timepoint <em>{1}</em></div>'.format(
            study.name, entity.timepoint))
        # > third element: the see more button
        self.w(u'<div class="col-md-3">')
        self.w(u'<button class="btn btn-danger" type="button" style="margin-top:8px" data-toggle="collapse" data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Acquisition center</dt><dd>{0}</dd>'.format(
            center.name))
        if len(related_subjects) == 1:
            subject = related_subjects[0]
            self.w(u'<dt>Gender</dt><dd>{0}</dd>'.format(
                subject.gender))
            self.w(u'<dt>Handedness</dt><dd>{0}</dd>'.format(
                subject.handedness))
            self.w(u'<dt>Age</dt><dd>{0}</dd>'.format(
                entity.age_of_subject))
        self.w(u'<dt>Identifier</dt><dd>{0}</dd>'.format(
            entity.identifier))
        self.w(u'<dt>Related runs</dt><dd>{0}</dd>'.format(
            " - ".join([x.view("incontext") for x in run_items])))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# Subject
###############################################################################

class NSSubjectOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("Subject")

    def cell_call(self, row, col):
        """ Create the NSSubjectOutOfContextView view line by line
        """
        # Get the assessment entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        assessment_items = entity.concerned_by

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' % self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Gender <em>{0}</em> - Handedness <em>{1}</em></div>'.format(
            entity.gender, entity.handedness))
        # > third element: the see more button
        self.w(u'<div class="col-md-3">')
        self.w(u'<button class="btn btn-danger" type="button" '
                'style="margin-top:8px" data-toggle="collapse" '
                'data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Related assessments</dt><dd>{0}</dd>'.format(
            " - ".join(['<a href="{0}">{1}</a>'.format(
                x.absolute_url(), x.identifier) for x in assessment_items])))
        # > create longitudinal summary views
        href = self._cw.build_url(
            "view", vid="highcharts-relation-summary-view",
            rql="Any A WHERE S eid '{0}', S assessments A".format(entity.eid),
            relations=["scans", "questionnaire_runs", "genomic_measures"],
            subject_attr="timepoint", object_attr="label",
            title="Acquisition status: {0}".format(entity.code_in_study))
        self.w(u'<dt>Acquisition summary</dt><dd><a href="{0}">'
                'status</a></dd>'.format(href))
        href = self._cw.build_url(
            "view", vid="highcharts-relation-summary-view",
            rql="Any A WHERE S eid '{0}', S assessments A".format(entity.eid),
            relations="related_processing", subject_attr="timepoint",
            object_attr="tool", title="Processing status: {0}".format(entity.code_in_study))
        self.w(u'<dt>Processing summary</dt><dd><a href="{0}">'
                'status</a></dd>'.format(href))
        href = self._cw.build_url(
            "view", vid="questionnaire-longitudinal-measures",
            rql=("Any QR WHERE S eid '{0}', S assessments A, "
                 "A questionnaire_runs QR".format(entity.eid)),
            patient_id=entity.code_in_study)
        self.w(u'<dt>Measure summary</dt><dd><a href="{0}">status</a>'
                '</dd>'.format(href))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# ProcessingRun
###############################################################################

class NSProcessingRunOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("ProcessingRun")

    def cell_call(self, row, col):
        """ Create the NSProcessingRunOutOfContextView view line by line
        """
        # Get the processing run entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        scan = entity.inputs[0]
        subject = scan.concerns[0]

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' % self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Name <em>{0}</em> - Tool <em>{1}</em> - Subject <em>{2}</em></div>'.format(
            entity.name, entity.tool, subject.code_in_study))
        # > third element: the see more button
        self.w(u'<div class="col-md-3">')
        self.w(u'<button class="btn btn-danger" type="button" style="margin-top:8px" data-toggle="collapse" data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Name</dt><dd>{0}</dd>'.format(
            entity.name))
        self.w(u'<dt>Tool</dt><dd>{0}</dd>'.format(
            entity.tool))
        self.w(u'<dt>Parameters</dt><dd>{0}</dd>'.format(
            entity.note))
        self.w(u'<dt>Relted scan</dt><dd>{0}</dd>'.format(
            scan.view("incontext")))
        self.w(u'<dt>Relted subject</dt><dd>{0}</dd>'.format(
            subject.view("incontext")))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# QuestionnaireRun
###############################################################################

class NSQuestionnaireRunOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("QuestionnaireRun")

    def cell_call(self, row, col):
        """ Create the NSQuestionnaireRunOutOfContextView view line by line
        """
        # Get the processing run entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        subject = entity.subject[0]
        questionnaire = entity.instance_of[0]

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' % self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'</div>')
        # > third element: the see more button
        self.w(u'<div class="col-md-3">')
        self.w(u'<button class="btn btn-danger" type="button" style="margin-top:8px" data-toggle="collapse" data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Related questionnaire</dt><dd>{0}</dd>'.format(
            questionnaire.view("incontext")))
        self.w(u'<dt>Relted subject</dt><dd>{0}</dd>'.format(
            subject.view("incontext")))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# Default
###############################################################################

class NSDefaultOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("CWSearch", "CWUpload")

    def cell_call(self, row, col):
        """ Create the default view line by line.
        """
        # Get the processing run entity
        entity = self.cw_rset.get_entity(row, col)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > add the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(
            entity.view("incontext")))
        self.w(u'</div>')
        # Close row item
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


def registration_callback(vreg):
    """ Update outofcontext views
    """
    vreg.register(NSDefaultOutOfContextView)
    vreg.register_and_replace(
        NSAssessmentOutOfContextView, AssessmentOutOfContextView)
    vreg.register_and_replace(NSScanOutOfContextView, ScanOutOfContextView)
    vreg.register(NSProcessingRunOutOfContextView)
    vreg.register_and_replace(
        NSQuestionnaireRunOutOfContextView, QuestionnaireRunOutOfContextView)
    vreg.register_and_replace(
        NSSubjectOutOfContextView, SubjectOutOfContextView)
