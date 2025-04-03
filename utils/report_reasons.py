from pyrogram.raw.types import (
    InputReportReasonSpam, InputReportReasonViolence, InputReportReasonChildAbuse,
    InputReportReasonPornography, InputReportReasonCopyright, InputReportReasonFake,
    InputReportReasonIllegalDrugs, InputReportReasonPersonalDetails, InputReportReasonOther
)

REPORT_REASONS = {
    "spam": InputReportReasonSpam(),
    "violence": InputReportReasonViolence(),
    "child_abuse": InputReportReasonChildAbuse(),
    "pornography": InputReportReasonPornography(),
    "copyright": InputReportReasonCopyright(),
    "fake": InputReportReasonFake(),
    "drugs": InputReportReasonIllegalDrugs(),
    "personal_data": InputReportReasonPersonalDetails(),
    "other": InputReportReasonOther()
}
