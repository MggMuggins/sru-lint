from debian import changelog

from sru_lint.plugins.plugin_base import Plugin
from sru_lint.common.feedback import FeedbackItem, Severity
from sru_lint.common.errors import ErrorCode
from sru_lint.common.logging import get_logger

class UCAPlugin(Plugin):
    """Checks for UCA-only uploads"""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("plugins.uca")
    
    def register_file_patterns(self):
        """Register file patterns this plugin should process."""
        self.add_file_pattern("debian/control")
    
    def process_file(self, processed_file):
        self.logger.info(f"Processing file: {processed_file.path}")

        # Get the added content from the changelog file
        added_lines = processed_file.source_span.content
        if not added_lines:
            self.logger.debug(f"No added lines in {processed_file.path}")
            return

        # Combine the added lines into changelog content
        changelog_content = "\n".join([line.content for line in added_lines])
        cl = changelog.Changelog(changelog_content)

        for entry in cl:
            suites = parse_distributions_field(str(entry.distributions))

            # TODO:
            # - Get a LPlib object for each of Build/Proposed/Release, checking
            #   to make sure the suites for this CL entry refer to a valid UCA
            #   pocket
            #   - Assume that the upload is LTS-only implicit in this check
            #     (i.e. oracular-epoxy doesn't exist)
            # - New version > version in Build
            # - Major version matches what's currently in the pocket
            # - Version ends in ~cloud1 (TDB, should we use cloud0 or cloud1?)

        # Your validation logic here
        #if some_condition:
        #    feedback = FeedbackItem(
        #        message="Issue description",
        #        rule_id=ErrorCode.MY_ERROR_CODE,
        #        severity=Severity.ERROR,
        #        span=processed_file.source_span
        #    )
        #    self.feedback.append(feedback)
