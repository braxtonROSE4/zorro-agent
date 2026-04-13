"""English (en) language patterns for learning signal detection.

Design principle: Wide recall, low cost. False positives are filtered by
confidence level; missed lessons are permanent data loss (high cost).
"""

# ── on-stop signal detection patterns ─────────────────────

CORRECTION_PATTERNS = [
    r"(?:you(?:'re| are) wrong|that's (?:wrong|incorrect|not right))",
    r"(?:the )?(?:correct|right|proper) (?:way|approach|method) (?:is|should be)",
    r"(?:that's not (?:how|what)|no[,.]+ that's (?:wrong|not))",
    r"(?:incorrect|wrong)[.,]",
    r"(?:you (?:got|have) (?:it|that|this) wrong|your (?:understanding|answer|response) is (?:wrong|incorrect|off))",
    r"(?:it )?should be .{2,40}(?:not|instead of)",
    r"(?:let me correct|correction|to clarify)",
    r"you (?:missed|overlooked|skipped|forgot|left out)",
]

INSIGHT_PATTERNS = [
    r"(?:the )?(?:lesson|takeaway|learning)(?: here)? (?:is|was)[:.]?",
    r"(?:from now on|going forward|in the future)[, ]+(?:always|make sure to|remember to)",
    r"(?:hit a (?:gotcha|pitfall|trap|snag)|stumbled (?:on|upon|into))",
    r"next time[, ]+(?:should|need to|remember to|make sure)",
    r"(?:key|important|critical) (?:finding|insight|realization|discovery) (?:is|was)",
    r"(?:didn't|never) (?:realize|know|notice) (?:that |about )?(?:before|until now)",
    r"(?:from now on|going forward)[, ]+(?:don't|avoid|never|stop)",
    r"(?:in retrospect|looking back|reflecting on)",
]

ERROR_PATTERNS = [
    r"I (?:got (?:it|that)|was) wrong",
    r"I shouldn't have",
    r"my (?:initial|earlier|previous|first) (?:approach|direction|thinking|assumption) was (?:wrong|off|flawed|incorrect)",
    r"(?:went down (?:the wrong|a bad) (?:path|road|direction)|took a detour|wasted time on)",
]

COGNITIVE_SHIFT_PATTERNS = [
    r"(?:I (?:thought|assumed|believed|expected)).{5,60}(?:but (?:actually|it turns out|in reality)|turns out)",
    r"(?:my )?(?:understanding|perspective|view|mental model) (?:has )?(?:changed|shifted|updated|evolved)",
    r"this (?:changes|updates|shifts) (?:my|the|our) (?:understanding|perspective|view|thinking)",
    r"(?:fundamental|core|basic) (?:misunderstanding|misconception|wrong assumption|flawed premise)",
]

METHOD_DISCOVERY_PATTERNS = [
    r"(?:the )?(?:correct|right|better|proper|effective) (?:way|approach|method|workflow|process) (?:is|should be)",
    r"this (?:method|approach|pattern|workflow|technique) (?:works|is) (?:really |much )?(?:well|great|effective|useful)",
    r"(?:from now on|going forward|always).{2,30}(?:first|before|should|start with)",
    r"(?:remember|make sure|note)[:.]?.{5,60}(?:before|then|only then|after that)",
]

ANTI_PATTERN_PATTERNS = [
    r"(?:don't|never|avoid|do not) (?:just |directly )?(?:start|jump into|dive into|skip|rush)",
    r"(?:anti[- ]pattern|common mistake|typical error|classic pitfall)",
    r"(?:absolutely|definitely|always) (?:don't|never|avoid)",
]

PROFILE_UPDATE_PATTERNS = [
    r"(?:now|currently|recently|this week|this month)\s+(?:focusing|working|mainly)\s+on",
    r"(?:shifted|moved|changed|switched)\s+(?:my\s+)?(?:focus|priority|attention)\s+to",
    r"(?:started|beginning|began)\s+(?:working on|doing|handling|leading)",
    r"(?:my\s+)?(?:main|primary|current)\s+(?:focus|priority|work)\s+(?:is|has been|shifted to)",
    r"(?:entered|moved to|started|reached|launched|shipped)\s+(?:V[0-9]+|(?:the\s+)?(?:next|new)\s+(?:phase|stage))",
    r"V[0-9]+\s+(?:started|launched|shipped|completed|done|finished)",
    r"(?:product|project)\s+(?:entered|moved to|reached|completed)\s+.{2,30}(?:phase|stage)",
    r"(?:took over|now responsible for|picked up|added)\s+.{2,30}(?:module|feature|area|domain)",
    r"(?:no longer|stopped|handed off|transferred)\s+(?:responsible for|handling|managing)",
    r"(?:my\s+)?(?:role|responsibilities|duties)\s+(?:changed|shifted|expanded|narrowed)",
]

COMPLETION_SIGNALS = [
    r"(?:that's (?:everything|all|it)|(?:all )?done|finished|completed|that covers it)",
    r"(?:anything else|need anything|other questions|what else)\??",
    r"if (?:there's nothing else|that's all)",
    r"(?:wrapping up|let's wrap)",
    r"(?:that should (?:be|cover|do)|we're (?:all )?(?:set|done|good))",
]

# ── transcript_analysis patterns ──────────────────────────

CORRECTION_SEQUENCE_PATTERNS = [
    r"(?:that's not (?:what|how)|no[,. ]+that's (?:not|wrong))",
    r"(?:you )?misunderst(?:ood|and)",
    r"(?:what I (?:meant|mean) (?:is|was)|I meant)",
    r"(?:I (?:didn't|did not) (?:ask|want) you to)",
    r"(?:start over|redo|undo|try again)",
    r"(?:you (?:got|have) (?:it|that) wrong)",
    r"(?:that's not what I (?:wanted|asked|need))",
    r"(?:you(?:'re| are) (?:wrong|mistaken|confused))",
    r"(?:incorrect|wrong|nope)[.,]",
    r"(?:your (?:understanding|interpretation|response) (?:is|was) (?:wrong|off|incorrect))",
]

FRAMEWORK_SIGNAL_PATTERNS = [
    r"(?:principles?|rules?|guidelines?|laws?)\s*[::]",
    r"(?:methodology|framework|approach)\s*[::]",
    r"(?:first|second|third|fourth|fifth).{2,30}(?:point|principle|step|rule|guideline)",
    r"(?:the )?(?:correct|right|proper) (?:process|workflow|procedure)\s*[::]",
    r"(?:anti[- ]pattern)\s*[::]",
    r"(?:step|phase|stage)\s*[1-5]\s*[::.])",
]

DECISION_RATIONALE_PATTERNS = [
    r"(?:chose|picked|selected|went with).{2,40}(?:instead of|rather than|over).{2,40}(?:because|since|due to|reason)",
    r"(?:the reason (?:for|why|is)|because).{5,60}(?:chose|picked|selected|decided|went with)",
    r"(?:chose|use|adopt|picked).{2,30}(?:instead of|rather than|over).{2,30}(?:reason|because|since|considering)",
]

RETRY_PATTERNS = [
    r"(?:redo|undo|start over|try again)",
    r"(?:one more time|again please|let's retry)",
    r"(?:change|fix|tweak|adjust) (?:it|this|that)",
    r"(?:that (?:doesn't|does not) work|nope|not (?:right|working|good))",
    r"(?:rework|revise|rewrite|rethink)",
    r"(?:different|another|alternative) (?:approach|way|method)",
    r"(?:try (?:something|a) (?:different|else|new))",
]

EXPLICIT_LESSON_PATTERNS = [
    r"(?:the )?(?:lesson|takeaway|learning)(?: here)? (?:is|was)\s*[:.]",
    r"(?:from now on|going forward|always|in the future)[, ]+(?:make sure|remember|need) to",
    r"(?:hit a (?:gotcha|pitfall|trap|snag)|stumbled (?:on|upon|into))",
    r"next time[, ]+(?:should|need to|remember to|make sure)",
    r"(?:key|important|critical) (?:finding|insight|realization|discovery) (?:is|was)",
    r"(?:didn't|never) (?:realize|know|notice) (?:that |about )?(?:before|until now)",
    r"(?:from now on|going forward)[, ]+(?:don't|avoid|never|stop)",
]

# ── rating_capture patterns ───────────────────────────────

SCORE_PATTERNS = [
    r"(?<![v#\d\-])(\d{1,2})\s*/\s*10",
    r"(?:score|rating|rate(?: it)?)\s*[:=]?\s*(\d{1,2})",
    r"(\d{1,2})\s*(?:out of 10|points?\b)",
    r"(?:give (?:it|this) (?:a |an )?|I'?d (?:say|rate(?: it)?) (?:a |an )?)(\d{1,2})\b",
]

SCORE_EXCLUDE_AFTER = [
    r"(?:am|pm)\b", r"th\b", r"st\b", r"nd\b", r"rd\b",
    r"%", r"x\b", r"k\b", r"px\b", r"GB?\b", r"MB?\b",
]

FRUSTRATION_SIGNALS = [
    r"(?:I (?:didn't|did not) (?:ask|want) you to)",
    r"(?:start over|redo|undo|try again)",
    r"(?:again|still) (?:wrong|incorrect|not right)",
    r"you (?:didn't|did not|don't|do not) (?:read|understand|listen|get it)",
    r"(?:this is (?:completely|totally|entirely)|that's (?:completely|totally)) (?:wrong|off|not what)",
    r"(?:that's not what I (?:said|meant|asked|wanted))",
]

SATISFACTION_SIGNALS = [
    r"(?:perfect|awesome|amazing|excellent|great job|well done|nailed it|fantastic|brilliant)",
    r"(?:exactly (?:what I (?:wanted|needed)|right|that)|that's (?:exactly |precisely )?(?:it|right|what I))",
    r"(?:great|good|nice|impressive) (?:work|job|output|result)",
]
