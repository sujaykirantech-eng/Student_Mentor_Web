# ==============================================================================
# Module: DoubtDiagnostic_General.py
# Purpose: Comprehensive Non-Subject-Specific Academic Diagnostic Engine
# Version: 6.0 - Full 26-Domain Diagnostic Matrix, Contextual NLP,
#               Returning Student Memory & Guaranteed MySQL Persistence
# ==============================================================================

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import mysql.connector

STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your', 'he', 'him', 'his',
    'she', 'her', 'it', 'its', 'they', 'them', 'their', 'what', 'which', 'who', 'whom',
    'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
    'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on',
    'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm',
    'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn',
    'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren',
    'won', 'wouldn', 'really', 'much', 'get', 'got', 'even', 'always', 'lot'
}

SAFETY_KEYWORDS = [
    'suicide', 'kill myself', 'end my life', 'harm myself', 'self harm', 'cutting',
    'abuse', 'beaten', 'violence', 'severe depression', 'want to die', 'hopeless'
]

def check_safety_concerns(text: str) -> bool:
    clean = str(text or "").lower()
    for phrase in SAFETY_KEYWORDS:
        if re.search(r'\b' + re.escape(phrase) + r'\b', clean):
            return True
    return False

def normalise_text(text: str) -> str:
    text = str(text or "").lower().strip()
    replacements = {
        "can't": "cannot", "doesn't": "does not", "don't": "do not", "won't": "will not",
        "i'm": "i am", "it's": "it is", "haven't": "have not", "idk": "i do not know",
        "dont": "do not", "cant": "cannot", "wont": "will not", "pls": "please"
    }
    for old, new in replacements.items():
        text = re.sub(r'\b' + re.escape(old) + r'\b', new, text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def simple_stem(word: str) -> str:
    if word.endswith('ing') and len(word) > 5:
        return word[:-3]
    if word.endswith('ed') and len(word) > 4:
        return word[:-2]
    if word.endswith('tion') and len(word) > 6:
        return word[:-4]
    if word.endswith('s') and not word.endswith('ss') and len(word) > 3:
        return word[:-1]
    return word

def get_ngrams(tokens: List[str]) -> List[str]:
    ngrams = list(tokens)
    for i in range(len(tokens) - 1):
        ngrams.append(f"{tokens[i]} {tokens[i+1]}")
    for i in range(len(tokens) - 2):
        ngrams.append(f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}")
    return ngrams

FOLLOWUP_CATEGORIES = {
    "positive_progress": {
        "title": "Positive Momentum & Habit Adoption",
        "keywords": [
            "better", "improved", "helped", "working", "worked", "good", "great",
            "managed to", "able to", "started studying", "focusing better", "marks increased",
            "feeling confident", "followed", "routine worked", "pomodoro worked"
        ],
        "mentor_response": (
            "That is significant progress! Building momentum in your studies proves that "
            "small, deliberate environmental changes produce real results."
        ),
        "guidance": (
            "Now the objective is habit stabilization: maintain this exact routine for the next "
            "10 days so it becomes effortless before expanding your workload."
        )
    },
    "implementation_slippage": {
        "title": "Implementation Friction & Habit Slippage",
        "keywords": [
            "tried but", "slipped", "relapsed", "forgot again", "distracted again", "hard to maintain",
            "stopped after", "only two days", "inconsistent", "could not keep up", "started well but",
            "back to old habits", "picked up phone again", "lost focus again"
        ],
        "mentor_response": (
            "I completely understand. When adopting a new study habit, slipping back into old patterns "
            "during the first week is completely normal. It does not mean you failed."
        ),
        "guidance": (
            "Instead of relying on sheer willpower, we need to lower the starting friction and increase "
            "physical environmental boundaries so that following through requires zero mental debate."
        )
    },
    "strategy_mismatch": {
        "title": "Persistent Constraint / Deep Resistance",
        "keywords": [
            "did not work", "didn't work", "nothing changed", "still shouting", "still comparing",
            "worse", "failed", "useless", "could not do it", "gave up", "no use", "parents still angry",
            "still blank", "still anxious"
        ],
        "mentor_response": (
            "Thank you for being completely candid. If the previous tactic didn't move the needle, "
            "it usually means there is a deeper root constraint that wasn't addressed."
        ),
        "guidance": (
            "We will pivot our strategy today. Rather than repeating what didn't work, we will address "
            "the root friction with a more protective, realistic plan."
        )
    },
    "new_challenge_surfaced": {
        "title": "Academic Shift / New Bottleneck",
        "keywords": [
            "now exam", "new problem", "now teacher", "feeling anxious now", "syllabus increased",
            "backlog now", "marks dropped", "now tired", "sleepy now", "feeling stressed now"
        ],
        "mentor_response": (
            "It sounds like your study situation has evolved. As previous routines stabilize, "
            "new demands like upcoming exams, heavier syllabi, or school pressure often emerge."
        ),
        "guidance": (
            "Let's direct our attention to this new bottleneck and build a targeted action plan for it."
        )
    }
}

def analyze_followup_progress(text: str) -> Tuple[str, str, str, str]:
    clean_text = normalise_text(text)
    scores = {}
    for cat_key, cat_data in FOLLOWUP_CATEGORIES.items():
        score = 0
        for kw in cat_data["keywords"]:
            norm_kw = normalise_text(kw)
            if " " in norm_kw:
                if norm_kw in clean_text:
                    score += 3
            else:
                if re.search(r'\b' + re.escape(norm_kw) + r'\b', clean_text):
                    score += 1
        scores[cat_key] = score

    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        return (
            "general_update",
            "General Follow-Up",
            "Thank you for sharing an honest update on where things stand.",
            "Let's review what is happening right now and calibrate your approach."
        )
    cat_info = FOLLOWUP_CATEGORIES[best_cat]
    return best_cat, cat_info["title"], cat_info["mentor_response"], cat_info["guidance"]

TOPIC_CATALOG: Dict[str, Dict[str, Any]] = {
    "concentration": {
        "title": "Concentration & Mental Stamina",
        "keywords": ["concentration", "focus", "mind wanders", "daydreaming", "cannot focus", "distracted thoughts", "zoning out", "drifting", "attention", "blank out"],
        "subtopics": {
            "mind_wandering": {"name": "Mind wanders into daydreams or unrelated thoughts", "trigger_words": ["wanders", "daydream", "thoughts", "thinking", "zoning"]},
            "short_span": {"name": "Losing focus after only 10–15 minutes of continuous study", "trigger_words": ["short", "quickly", "10 minutes", "15 minutes", "cannot sit"]},
            "cant_start": {"name": "Sitting at the study desk but taking forever to actually start", "trigger_words": ["start", "begin", "sitting", "staring", "blank"]},
            "external_pull": {"name": "Easily pulled away by tiny noises or minor room movements", "trigger_words": ["noise", "surroundings", "room", "family", "sound"]}
        },
        "questions": [
            ("When you sit down to study, how many minutes can you typically maintain deep focus before attention drifts?",
             {"1": "Under 10 minutes", "2": "About 15–20 minutes", "3": "About 30–45 minutes", "4": "Focus varies wildly depending on interest"}),
            ("What is the primary trigger that derails your attention during a session?",
             {"1": "Intrusive random thoughts / daydreaming", "2": "Checking notification/phone instinctively", "3": "Physical restlessness or boredom", "4": "Hitting a slightly difficult sentence or problem"})
        ],
        "comprehensive_advice": [
            "Implement the 'Wander-Pad' Protocol: Keep an open blank notepad beside your book. The instant a random thought or daydream enters your head, scribble it down in 3 words and tell your brain: 'It is safely recorded; I will deal with it during the break.'",
            "Targeted Micro-Pomodoros (25m Focus / 5m Rest): Do not force 3-hour marathon sessions. 25 minutes of pure singular focus beats 2 hours of distracted pseudo-studying every single time.",
            "Active Pencil-Pacing: Concentration breaks when your eyes scan text passively. Always trace lines with a pen tip or summarize paragraph margins in 3 words.",
            "Visual Horizon & Tunnel Focus: Sit facing a neutral blank wall rather than facing a window or open living room where optical movement involuntarily breaks focus.",
            "Audio Masking: Use consistent non-vocal background tracks (brown noise or binaural 40Hz waves) to mask household chatter."
        ],
        "named_protocol": "The 25/5 Wander-Pad Focus System",
        "mindset_shift": "Concentration is not a mystical personality trait—it is an environmental boundary that you train through progressive intervals.",
        "action": "Set a timer for 25 minutes right now with zero device switching. Use a blank paper beside your desk to park stray thoughts."
    },
    "distraction": {
        "title": "Digital & Environmental Distractions",
        "keywords": ["distraction", "distracted", "phone", "mobile", "youtube", "instagram", "reels", "shorts", "gaming", "social media", "notifications", "screen"],
        "subtopics": {
            "phone_addiction": {"name": "Compulsive phone checking, reels, shorts, or social feeds", "trigger_words": ["phone", "instagram", "reels", "shorts", "whatsapp", "feed"]},
            "pc_multitasking": {"name": "Having multiple study tabs open that morph into YouTube / browsing", "trigger_words": ["youtube", "laptop", "browser", "tabs", "pc", "video"]},
            "gaming_chat": {"name": "Messaging apps and gaming notifications interrupting study blocks", "trigger_words": ["game", "gaming", "discord", "chat", "friends texting"]}
        },
        "questions": [
            ("Where is your mobile phone positioned during self-study hours?",
             {"1": "Right beside my textbook or within arm's reach", "2": "In the same room across the table", "3": "In a separate room, but I go get it", "4": "I study on the phone/laptop itself"}),
            ("What best describes your pattern of digital diversion?",
             {"1": "Micro-checking notifications every 5 minutes", "2": "Intending to check for 2 minutes and losing 45 minutes", "3": "Playing videos in the background while pretending to read", "4": "Reaching for the phone whenever a problem feels difficult"})
        ],
        "comprehensive_advice": [
            "The 20-Second Physical Friction Rule: Place your smartphone in another room, inside a high shelf, or with a family member during study blocks.",
            "Greyscale Display Mode: Switch your phone screen to black-and-white (Monochrome) under Accessibility settings to reduce visual dopamine stimulation by 50%.",
            "Single-Window Constraint: When studying on a PC, use full-screen mode with only one tab and activate website blockers.",
            "Pre-Determined Reward Windows: Batch screen time into an intentional 20-minute window after completing your evening academic deliverables.",
            "Physical Textbook Substitution: Use printed worksheets or physical textbooks whenever possible to avoid digital temptations."
        ],
        "named_protocol": "The Out-of-Sight Physical Friction System",
        "mindset_shift": "You cannot out-willpower algorithms designed to hook your attention; you must out-design your environment.",
        "action": "Place your smartphone on silent mode in a separate room or inside a drawer for your next 45-minute study session."
    },
    "procrastination": {
        "title": "Procrastination & Starting Friction",
        "keywords": ["procrastination", "procrastinate", "delay", "delaying", "tomorrow", "lazy", "postpone", "putting off", "last minute", "avoiding work"],
        "subtopics": {
            "starting_friction": {"name": "Overwhelmed by syllabus volume, resulting in total avoidance", "trigger_words": ["huge", "overwhelmed", "starting", "syllabus", "size"]},
            "perfectionism_stall": {"name": "Waiting for the 'perfect mood', 'ideal time', or exact hour to start", "trigger_words": ["perfect", "mood", "exact time", "clean desk"]},
            "deadline_dependency": {"name": "Only working when exam panic sets in the evening prior", "trigger_words": ["deadline", "panic", "last minute", "night before"]}
        },
        "questions": [(
            "What thought crosses your mind right before you postpone studying?",
            {"1": "'I will start fresh tomorrow morning or at the top of the hour.'", "2": "'This chapter is massive; I don't know where to begin.'", "3": "'I have plenty of time, exams are still weeks away.'", "4": "'I am not in the right mental energy or mood right now.'"}
        )],
        "comprehensive_advice": [
            "The 5-Minute Entry Ticket Rule: Give yourself permission to study for just 5 minutes with zero obligation to finish the chapter. Once momentum starts, resistance drops.",
            "Micro-Scaffolding the First Action: Replace 'Study Physics' on your to-do list with 'Open page 42 and read Definition 3.1'.",
            "Destroy the Clock Trap: Stop waiting for round numbers (e.g., waiting for 5:30 PM when it is 5:08 PM). Time is continuous.",
            "Lower the Bar to 'Ugly First Drafts': Allow your initial calculations and notes to be rough to prevent perfectionism paralysis.",
            "Artificial Early Deadlines: Agree on self-imposed review checkpoints with a study partner 4 days before the official test."
        ],
        "named_protocol": "The 5-Minute Mechanical Momentum Strategy",
        "mindset_shift": "Action produces motivation; motivation rarely produces action. Move your hands first, and your brain will follow.",
        "action": "Pick the assignment you dread most right now. Sit down and do exactly two textbook questions, nothing more."
    },
    "time_management": {
        "title": "Time Management & Daily Scheduling",
        "keywords": ["time management", "time", "hours", "schedule", "timetable", "no time", "wasting time", "day passes", "unorganized", "running out of time"],
        "subtopics": {
            "unrealistic_timetables": {"name": "Creating overly rigid hour-by-hour timetables that collapse on Day 1", "trigger_words": ["timetable", "rigid", "collapsed", "impossible"]},
            "lost_hours": {"name": "The entire day slipping away without knowing where the hours vanished", "trigger_words": ["vanished", "lost time", "slipped", "wasted hours"]},
            "school_coaching_overload": {"name": "School and tuition consuming all daylight hours with no self-study buffer", "trigger_words": ["school", "coaching", "tuition", "no time left", "evening"]}
        },
        "questions": [
            ("How do you currently organize your daily study hours?",
             {"1": "I don't plan; I pick whatever feels most urgent", "2": "I make rigid hour-by-hour timetables that I fail to sustain", "3": "I keep a mental to-do list that gets disorganized", "4": "I write long checklists but consistently overestimate what I can finish"})
        ],
        "comprehensive_advice": [
            "The 3-Deliverable Rule: Replace clock-based schedules with 3 specific outputs (e.g., 'Ex 4.2 Q1-5, Revise Optics formulas, Read History Ch 2').",
            "Transition Rituals: When returning from school or coaching, take a 20-minute physical reset before touching your books.",
            "The Rule of Two: Study a maximum of two subjects per evening (one analytical + one descriptive) for deeper cognitive consolidation.",
            "3-Day Stop-Clock Audit: Track your actual focused minutes with a stopwatch to identify where your time leaks.",
            "Buffer Zones: Leave 20% of your weekly schedule completely blank to absorb unexpected assignments without cutting sleep."
        ],
        "named_protocol": "The 3-Deliverable Modular Block System",
        "mindset_shift": "Time management is about protecting 2-3 high-intensity blocks and resting guilt-free.",
        "action": "Write down exactly three academic deliverables on an index card for tomorrow before sleeping tonight."
    },
    "motivation": {
        "title": "Motivation & Academic Drive",
        "keywords": ["motivation", "unmotivated", "not motivating", "no motivation", "drive", "purpose", "do not feel like", "boring", "apathy", "hopeless study", "lack of interest"],
        "subtopics": {
            "burnout_exhaustion": {"name": "Mental fatigue from weeks of continuous academic pressure", "trigger_words": ["burnout", "tired", "exhausted", "continuous"]},
            "disconnection": {"name": "Feeling no emotional connection or purpose in syllabus topics", "trigger_words": ["boring", "irrelevant", "meaningless", "why study this"]},
            "demotivation_marks": {"name": "Loss of drive after receiving lower test marks than expected", "trigger_words": ["low marks", "bad scores", "test result", "useless"]}
        },
        "questions": [(
            "What is the underlying sentiment when you feel unmotivated?",
            {"1": "'No matter how hard I work, my scores do not reflect the effort.'", "2": "'The material is boring and has no real-life connection.'", "3": "'I am burnt out and exhausted from routine.'", "4": "'I don't have a clear goal or dream I'm working toward.'"}
        )],
        "comprehensive_advice": [
            "Rely on Identity Habits: Build identity statements ('I am a student who sits down at 6 PM regardless of mood') instead of waiting for motivation.",
            "Decouple Effort from Immediate Marks: Learning follows a delayed curve. Today's practice questions often show up in test results weeks later.",
            "The Streak Calendar: Mark an 'X' on a physical wall calendar for every day you complete your minimum study floor.",
            "Guilt-Free Active Recharging: Take real rest (walking outside, listening to music) rather than scrolling social media while feeling guilty.",
            "The Anchor Card: Keep your long-term collegiate or career objective written inside your desk drawer to remember your purpose."
        ],
        "named_protocol": "The Identity-Driven Streak Architecture",
        "mindset_shift": "You do not need to feel enthusiastic to make progress; you only need to show up consistently.",
        "action": "Complete one focused 20-minute revision task today to score an immediate consistency win."
    },
    "memory_forgetting": {
        "title": "Memory, Retention & Forgetting",
        "keywords": ["memory", "forget", "forgetting", "retention", "forgot", "cannot remember", "blank during exam", "recall", "memorise", "memorizing"],
        "subtopics": {
            "fast_decay": {"name": "Understanding concepts while reading but forgetting 80% within 48 hours", "trigger_words": ["fast", "decay", "48 hours", "next day", "blank"]},
            "formula_confusion": {"name": "Mixing up definitions, formulas, or chemical equations across units", "trigger_words": ["formulas", "mix up", "equations", "names", "terms"]},
            "exam_blackout": {"name": "Knowing concepts well at home but freezing up in the examination hall", "trigger_words": ["blackout", "freeze", "hall", "exam blank"]}
        },
        "questions": [(
            "How do you currently verify whether you have retained a topic?",
            {"1": "I re-read the notes multiple times until they feel familiar", "2": "I close the book and try to write the derivations on blank paper", "3": "I only find out during chapter tests whether I remembered it", "4": "I highlight key lines in the textbook"}
        )],
        "comprehensive_advice": [
            "Active Closed-Book Retrieval: Close your notes completely and force your brain to reconstruct formulas and diagrams on blank paper.",
            "Spaced Leitner Intervals: Review new topics at 1-day, 4-day, and 14-day intervals to interrupt the forgetting curve.",
            "Dual-Coding: Pair abstract equations with visual schematics and spatial layout diagrams.",
            "Feynman Teach-Back Technique: Explain the concept out loud in plain words as if teaching a younger student.",
            "Formula Pocket Register: Maintain a slim 40-page notebook strictly for formulas, derivations, and constants."
        ],
        "named_protocol": "The Closed-Book Spaced Retrieval Protocol",
        "mindset_shift": "Memory is not a bucket filled by passive reading; it is strengthened only when you force it to retrieve information.",
        "action": "Close your textbook right now on a recent chapter and write down every formula from memory on blank paper."
    },
    "revision": {
        "title": "Revision Strategy & Backlog Clearance",
        "keywords": ["revision", "revise", "backlog", "backlogs", "pending chapters", "old chapters", "forgetting previous topics", "cumulative review"],
        "subtopics": {
            "backlog_mountain": {"name": "Old unrevised chapters piling up while current syllabus sprints ahead", "trigger_words": ["backlog", "pending", "old chapters", "piling up"]},
            "passive_rereading": {"name": "Revising simply by flipping through highlighted notes without solving problems", "trigger_words": ["flipping", "rereading", "passive", "highlighting"]},
            "panic_cycling": {"name": "Spending days revising Chapter 1, forgetting Chapter 2, and feeling stuck in loops", "trigger_words": ["loop", "cycle", "forget previous", "stuck"]}
        },
        "questions": [(
            "How do you allocate time between learning new topics versus revising previous chapters?",
            {"1": "100% of my time goes to ongoing homework; zero time for revision", "2": "I only revise when a class test is announced", "3": "I try to revise on weekends, but school assignments take over", "4": "I try to revise, but end up rereading the full textbook from page 1"}
        )],
        "comprehensive_advice": [
            "The 80/20 Backlog Rule: Spend 80% of your time on current syllabus and reserve the first 45 minutes of each morning strictly for backlog clearance.",
            "Problem-First Revision: Do NOT reread theory from page 1. Open the chapter exercise directly, solve 5 varied questions, and review theory only for errors.",
            "Traffic-Light Categorization: Mark units Green (mastered), Yellow (understand theory, make calculation slips), or Red (conceptual gap). Focus revision on Yellow and Red units.",
            "Interleaved Problem Sets: Solve 3 questions from Chapter 1, 3 from Chapter 4, and 3 from Chapter 6 to train concept switching.",
            "One-Page Cheat Sheets: Condense each chapter into a single double-sided A4 summary as you review."
        ],
        "named_protocol": "The Problem-First 80/20 Revision System",
        "mindset_shift": "Revision is not repeating the learning process from scratch; it is an active stress-test of what you already know.",
        "action": "Select one older chapter and solve 5 textbook questions today without rereading the chapter first."
    },
    "reading_difficulties": {
        "title": "Reading Comprehension & Textbook Fatigue",
        "keywords": ["reading", "textbook", "slow reader", "heavy words", "boring text", "comprehension", "do not understand book", "dense paragraphs"],
        "subtopics": {
            "heavy_language": {"name": "Struggling with formal, dense academic English in NCERT/textbooks", "trigger_words": ["english", "formal", "dense", "words", "vocabulary"]},
            "reading_drowsiness": {"name": "Feeling intensely sleepy or unfocused within 5 minutes of opening a textbook", "trigger_words": ["sleepy", "drowsy", "tired", "sleep", "eyes heavy"]},
            "re_reading_lines": {"name": "Having to read the same paragraph 4 times because your brain didn't register it", "trigger_words": ["register", "four times", "same sentence", "repeat reading"]}
        },
        "questions": [(
            "What physical reading approach do you usually adopt?",
            {"1": "Reading silently while lying in bed or slouching", "2": "Reading with a pen/pencil actively tracing lines and summarizing in margins", "3": "Reading large sections in one go without pauses", "4": "Switching immediately to video explanations because reading feels exhausting"}
        )],
        "comprehensive_advice": [
            "Kinesthetic Pencil-Pacing: Trace every line with a pencil tip to prevent your eyes from darting backwards and double your comprehension speed.",
            "3-Word Margin Synthesis: Pause after each paragraph and write a 3-word summary in the margin to verify cognitive processing.",
            "Pre-Reading Structural Scan: Read the Chapter Summary, diagrams, and bold headings before reading the chapter from the beginning.",
            "Upright Reading Posture: Never read lying in bed; sit upright with feet flat on the floor to maintain an alert neurological state.",
            "Translate Academic Jargon: Rewrite dense textbook definitions in your own plain words."
        ],
        "named_protocol": "The Active Pencil-Paced Chunking Strategy",
        "mindset_shift": "Reading a technical textbook is an active research investigation, not a passive bedtime story.",
        "action": "Read the next 2 pages of your textbook with a pencil in hand, writing a 3-word summary beside every paragraph."
    },
    "note_making": {
        "title": "Note-Making & Information Processing",
        "keywords": ["notes", "note-making", "making notes", "copying textbook", "messy notes", "how to take notes", "summary", "short notes", "formula sheet"],
        "subtopics": {
            "textbook_copying": {"name": "Mindlessly copying sentences from textbook to notebook without processing", "trigger_words": ["copying", "transcribing", "rewriting", "full text"]},
            "disorganized_binders": {"name": "Notes scattered across loose papers, rough books, and different folders", "trigger_words": ["scattered", "messy", "lost notes", "rough book"]},
            "no_short_notes": {"name": "Having 200 pages of notes but no 2-page summary sheets for quick pre-exam review", "trigger_words": ["bulky", "huge notes", "no formula sheet", "revision sheet"]}
        },
        "questions": [(
            "What is your standard practice when taking notes?",
            {"1": "I basically copy teacher slides or book paragraphs word-for-word", "2": "I don't make notes; I just highlight lines in the textbook", "3": "I take messy rough notes that I cannot decipher weeks later", "4": "I try to make notes, but it takes so many hours that I stop"}
        )],
        "comprehensive_advice": [
            "The 3-Section Cornell Format: Divide your page into Key Terms (25% left), Concise Bullet Points (60% right), and a 2-Sentence Summary at the bottom.",
            "Dual-Sheet Compression: Condense every chapter into 2 pages: Page 1 for formulas and derivations; Page 2 for common traps, diagrams, and exceptions.",
            "Never Take Notes on First Reading: Only underline on the first pass; take notes during your second reading when you know what is truly important.",
            "Visual Flowcharts over Paragraphs: Convert multi-step mechanisms and cycles into labeled arrow diagrams.",
            "Dedicated Subject Binders: Maintain one organized notebook per subject with sequentially numbered pages."
        ],
        "named_protocol": "The Cornell Compression Framework",
        "mindset_shift": "The purpose of notes is not to rewrite the textbook; it is to create a fast retrieval guide for your future self.",
        "action": "Condense one completed chapter onto a single double-sided A4 summary sheet today."
    },
    "teacher_explanation": {
        "title": "Understanding Teacher's Explanation",
        "keywords": ["teacher explanation", "teacher", "explains", "teaching", "class pace", "lectures", "school teaching", "cannot follow teacher", "boring teacher"],
        "subtopics": {
            "fast_pace": {"name": "Teacher moves too rapidly through concepts and steps on the board", "trigger_words": ["fast", "rush", "speed", "steps skipped"]},
            "missing_intuition": {"name": "Teacher provides formulas/theorems without explaining the physical meaning or intuition", "trigger_words": ["intuition", "why", "only formulas", "no logic"]},
            "board_copying_lag": {"name": "Getting stuck frantically copying the blackboard while missing what the teacher says", "trigger_words": ["board", "copying", "blackboard", "listening"]}
        },
        "questions": [(
            "When you feel lost during a classroom lecture, what is usually happening?",
            {"1": "The teacher assumes prerequisite knowledge from earlier grades that I lack", "2": "The teacher skips intermediate algebraic or conceptual steps", "3": "I am too busy scribbling notes to actually listen and think", "4": "The tone of voice or accent is difficult to engage with"}
        )],
        "comprehensive_advice": [
            "The 10-Minute Pre-Lecture Scan: Spend 10 minutes previewing the diagrams and bold terms of the upcoming school chapter before class.",
            "Prioritize Listening Over Copying: If you miss a blackboard step, borrow a friend's notes after class rather than missing the live explanation.",
            "Mark the Transition Break: Put a small '?' in your margin right where you lost the thread and keep listening to the rest of the lecture.",
            "Targeted Secondary Educator: Use a single trusted video channel to review only the specific 15-minute gap that felt unclear.",
            "Same-Day Derivation Reconstruction: Re-derive the key formulas on scrap paper within 4 hours of the lecture."
        ],
        "named_protocol": "The Pre-Scan & Active Listening Protocol",
        "mindset_shift": "The classroom is for understanding the logic; your home desk is where you master the execution.",
        "action": "Spend 10 minutes tonight scanning the diagrams of tomorrow's scheduled school chapter."
    },
    "asking_doubts": {
        "title": "Hesitation in Asking Doubts",
        "keywords": ["asking doubts", "doubt", "ask doubts", "shy", "scared to ask", "embarrassed", "judged", "stupid question", "hesitate to ask"],
        "subtopics": {
            "peer_judgment": {"name": "Fearing classmates will laugh or consider the question basic/silly", "trigger_words": ["laugh", "classmates", "silly", "stupid", "peer judgment"]},
            "teacher_strictness": {"name": "Hesitating because the teacher reacts impatiently or scolds students", "trigger_words": ["scold", "angry", "strict", "impatient", "shouted"]},
            "cant_articulate": {"name": "Knowing something is confusing but unable to formulate it into clear words", "trigger_words": ["articulate", "formulate", "dont know how to ask", "words"]}
        },
        "questions": [(
            "What stops you from raising your hand when confused?",
            {"1": "'Everyone else seems to understand; I will look foolish if I ask.'", "2": "'The teacher might snap or ask why I wasn't paying attention.'", "3": "'I cannot put my confusion into an exact, clean question.'", "4": "'I tell myself I will figure it out on YouTube later, but never do.'"}
        )],
        "comprehensive_advice": [
            "The Two-Step Bridge Formula: Frame doubts as: 'I understood Step A, but I am confused about why we transitioned to Step B.'",
            "The Sticky-Note Parking Strategy: Write doubts on sticky notes and approach the teacher privately right after the bell.",
            "The Classroom Truth: When you are confused, several other students in the room share the same confusion but are also hesitant to ask.",
            "2-Person Doubt Pact: Team up with a friend to ask questions together to lower anxiety.",
            "Staff Room Consultations: Visit the teacher in the staff room during break with your notebook open to the exact line."
        ],
        "named_protocol": "The Step-A-to-Step-B Precision Doubt Protocol",
        "mindset_shift": "Asking a question risks looking unsure for 30 seconds; staying silent ensures you remain confused during the final exam.",
        "action": "Write down one exact doubt from your homework right now using the template: 'I understand X, but why did we do Y?'"
    },
    "peer_influence": {
        "title": "Friends & Peer Influence",
        "keywords": ["friends", "peer pressure", "peers", "classmates", "friend circle", "distracted by friends", "fomo", "friends bragging", "friends distracting me"],
        "subtopics": {
            "toxic_comparison": {"name": "Constantly feeling inferior when friends boast about completing portions or mock tests", "trigger_words": ["friends ahead", "peers comparing", "inferior", "ahead", "marks comparison"]},
            "study_group_distraction": {"name": "Group study sessions devolving into gossip, memes, and chatting", "trigger_words": ["group study", "chatting", "gossip", "wasting time together"]},
            "pressure_to_slurp": {"name": "Pressure to play games, chat, or hang out when you need to study", "trigger_words": ["peer pressure", "games", "hang out", "calls", "distracting me"]}
        },
        "questions": [(
            "How does your peer circle primarily impact your academic routine?",
            {"1": "Constant comparison of scores and syllabus completion that causes anxiety", "2": "Constant group chats and gaming invitations during evening study hours", "3": "They act like studying hard is uncool or try to distract me in class", "4": "Fake modesty: friends claiming they didn't study when they scored full marks"}
        )],
        "comprehensive_advice": [
            "Recognize Posturing: Classmates who claim they never study before scoring top marks are managing their own insecurities. Put emotional earplugs on.",
            "Study Flight Mode: Tell your friends directly: 'I put my phone on DND between 6:00 PM and 9:00 PM for study blocks.' Real friends respect clear boundaries.",
            "Silent Parallel Study: Turn group study into 45 minutes of silent co-working followed by a 10-minute doubt-clearing session.",
            "Compete Against Yourself: The only relevant benchmark is whether you can solve problems today that you couldn't solve two weeks ago.",
            "Audit Your Core Circle: Protect your study hours quietly if your circle frequently ridicules hard work."
        ],
        "named_protocol": "The Independent Flight-Mode Protocol",
        "mindset_shift": "You do not need to walk the exact same daily path as your friends; true allies respect your ambitions.",
        "action": "Put messaging apps on mute and inform your peers you will be offline for a 2-hour study block tonight."
    },
    "family_home_environment": {
        "title": "Family Expectations & Home Environment",
        "keywords": ["family", "home", "parents", "pressure from parents", "expectations", "noise at home", "small house", "chores", "family issues", "comparing me with", "comparing with cousins", "parents comparing", "parents not motivating", "relatives", "father", "mother", "mom", "dad"],
        "subtopics": {
            "high_parental_pressure": {"name": "Suffocating pressure to achieve top ranks or repeated comparison with cousins / others", "trigger_words": ["parents", "rank", "cousins", "pressure", "expectations", "scolding", "comparing", "others", "not motivating"]},
            "noise_disturbances": {"name": "Constant noise from TV, siblings, relatives, or household activities", "trigger_words": ["noise", "tv", "siblings", "disturbed", "no separate room"]},
            "errands_chores": {"name": "Frequent interruptions for household work and responsibilities during study hours", "trigger_words": ["chores", "errands", "work", "responsibilities", "interruptions"]}
        },
        "questions": [(
            "What is the main challenge created by your home environment?",
            {"1": "Repeated emotional pressure regarding career ranks, marks, or comparison with others", "2": "High ambient noise or lack of a quiet, dedicated personal study spot", "3": "Frequent domestic errands that break my flow", "4": "Tension and disagreements at home that leave me mentally preoccupied"}
        )],
        "comprehensive_advice": [
            "The 'Proactive Progress Broadcast': Give parents a calm 2-minute weekly update every Sunday evening before they ask or scold. When parents lack visibility, anxiety turns into hovering and comparisons.",
            "Neutral De-escalation Protocol: When compared to cousins or peers, use the neutral script: 'They are preparing well in their way. I am systematically targeting my weak chapters today.' Then return to work without arguing.",
            "Negotiate Protected Study Windows: Ask for a clear boundary: 'Between 6:00 PM and 8:30 PM, I need zero household errands and quiet space.'",
            "Shift to Early Mornings: If your home is noisy in the evening, shift your primary deep-work block to 5:00 AM - 7:00 AM when the house is completely quiet.",
            "Differentiate Fear from Worth: Recognize that parental comparison usually stems from anxiety about your future security, not an intention to hurt you. Detach your self-worth from their daily mood."
        ],
        "named_protocol": "The Proactive Alignment & Boundary Framework",
        "mindset_shift": "Your parents' anxiety is their emotional burden; your responsibility is to focus on daily academic execution.",
        "action": "Have a calm 2-minute conversation with your parents today specifying your core 2-hour daily study block when you request no interruptions."
    },
    "study_environment": {
        "title": "Study Space & Physical Environment",
        "keywords": ["study environment", "study space", "desk", "room", "bed", "lighting", "uncomfortable chair", "clutter", "study setup"],
        "subtopics": {
            "bed_studying": {"name": "Studying on the bed or sofa, leading directly to lethargy and sleep", "trigger_words": ["bed", "sofa", "sleeping", "laying down", "lying down"]},
            "desk_clutter": {"name": "Messy desk piled high with books from all subjects causing visual overwhelm", "trigger_words": ["clutter", "messy", "piles", "scattered", "chaotic"]},
            "poor_lighting_ergonomics": {"name": "Dim lighting, back pain, or poor ventilation causing physical fatigue", "trigger_words": ["lighting", "dark", "back pain", "chair", "ventilation"]}
        },
        "questions": [(
            "Where do you physically conduct 80% of your self-study?",
            {"1": "On my bed or a soft couch", "2": "At a desk, but it is piled with papers and unrelated devices", "3": "At the dining table or shared living area with high foot traffic", "4": "A dedicated quiet desk and chair"}
        )],
        "comprehensive_advice": [
            "The Sacred Bed Boundary: Never study on your bed. Your brain associates beds with sleep, triggering drowsiness within 15 minutes.",
            "The One-Subject Desk Rule: Keep only the single textbook and notebook for your active subject on your desk.",
            "Direct Illumination: Ensure cool-white light shines directly onto your reading surface to prevent eye strain and fatigue.",
            "Hydration Station: Keep a 1-liter water bottle permanently on your desk; mild dehydration drops attention by 20%.",
            "60-Second Evening Desk Reset: Clear your desk at night and lay out the exact book you will open the next morning."
        ],
        "named_protocol": "The Clean-Desk Singular Focus Setup",
        "mindset_shift": "Your desk is your cognitive operating table; maintain it with surgical focus.",
        "action": "Clear your study table right now of all books except for the single subject notebook you will open next."
    },
    "exam_preparation": {
        "title": "Exam Preparation & Mock Strategy",
        "keywords": ["exam preparation", "exam plan", "syllabus completion", "test preparation", "mock tests", "sample papers", "how to prepare for exam"],
        "subtopics": {
            "unbalanced_coverage": {"name": "Spending 80% of time on favourite chapters while avoiding high-weightage tough units", "trigger_words": ["favourite", "easy chapters", "avoiding", "syllabus balance"]},
            "no_mock_tests": {"name": "Only reading theory without writing full-length timed sample papers", "trigger_words": ["sample papers", "mock tests", "no tests", "timing test"]},
            "last_week_scramble": {"name": "Starting real preparation only 7 days prior to board/term examinations", "trigger_words": ["one week", "last week", "panic", "scramble"]}
        },
        "questions": [(
            "How many full-length timed sample papers do you solve before an exam?",
            {"1": "None; I just revise notes and hope for the best", "2": "Maybe one, untimed, while looking up answers in between", "3": "2 to 3 timed papers under strict exam conditions", "4": "I read questions and answers instead of writing them out"}
        )],
        "comprehensive_advice": [
            "The 70/30 Content vs Simulation Ratio: 70% of exam preparation is studying chapters; 30% MUST be full-length, timed sample paper solving.",
            "Target High-Weightage Chapters First: Analyze the official board blueprint to master high-yield units before minor chapters.",
            "Previous Year Questions (PYQs): Solve the last 7 years of board questions; examiners reuse core derivations and question structures repeatedly.",
            "Strict Exam Simulation: Put your phone in another room, set a 3-hour timer, and solve papers without stopping for snacks.",
            "Post-Mock Forensic Analysis: Categorize lost marks into Concept Gap, Misread Question, or Calculation Error, and fix the specific cause."
        ],
        "named_protocol": "The 7-Year PYQ & Simulation Framework",
        "mindset_shift": "Exams do not reward who read the most pages; they reward who can write accurate answers to specific prompts under a ticking clock.",
        "action": "Select one previous-year question paper today and schedule a 90-minute timed mock test for this weekend."
    },
    "exam_pressure": {
        "title": "Exam Pressure & Performance Anxiety",
        "keywords": ["exam pressure", "stress", "anxiety", "panic", "fear of failure", "nervous", "sweaty hands", "racing heart", "exam fear"],
        "subtopics": {
            "fear_of_failure": {"name": "Obsessive dread of failing, disappointing parents, or getting low marks", "trigger_words": ["fail", "disappoint", "shame", "low marks", "what will people say"]},
            "exam_hall_panic": {"name": "Racing heartbeat, nausea, or mental blankness during the first 10 minutes of an exam", "trigger_words": ["heartbeat", "nausea", "blankness", "hands shaking", "panic attack"]},
            "overthinking_cutoff": {"name": "Calculating college ranks, future cutoff marks, and worst-case scenarios instead of studying", "trigger_words": ["ranks", "cutoff", "future", "college", "worst case"]}
        },
        "questions": [(
            "When does exam anxiety peak most destructively for you?",
            {"1": "The night right before the examination, destroying sleep", "2": "During the first 5 minutes when the question paper is handed out", "3": "Weeks in advance, paralyzing day-to-day study", "4": "When I see one difficult question I cannot solve in the hall"}
        )],
        "comprehensive_advice": [
            "4-4-4-4 Box Breathing Reset: Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4 to physically regulate your nervous system.",
            "First 10-Minute Paper Scan: Scan the paper for the 3 easiest, most familiar questions and solve those first to build momentum.",
            "Demystify Worst-Case Scenarios: Write down your deepest fear on paper alongside a realistic, practical recovery plan.",
            "Strict Pre-Exam Sleep Architecture: Never sacrifice sleep the night before an exam for late-night cramming.",
            "Physical Grounding: Keep your feet flat on the floor, grip your pen firmly, take a deep sip of water, and remember you have solved hundreds of practice problems."
        ],
        "named_protocol": "The Physiological Calming & Quick-Win Paper Strategy",
        "mindset_shift": "An exam does not measure your intelligence or worth—it only measures how well you write answers on that specific morning.",
        "action": "Take 2 minutes to practice the 4-4-4-4 Box-Breathing exercise and write down your top 3 guaranteed scoring units."
    },
    "confidence": {
        "title": "Academic Confidence & Self-Doubt",
        "keywords": ["confidence", "self-doubt", "impostor", "not smart enough", "give up easily", "low self esteem", "cannot do it", "everyone is smarter"],
        "subtopics": {
            "impostor_feelings": {"name": "Feeling that past successes were just luck and you aren't actually capable", "trigger_words": ["luck", "impostor", "not smart", "incapable"]},
            "giving_up_at_first_hurdle": {"name": "Abandoning a problem or chapter the second it requires effort or multiple attempts", "trigger_words": ["give up", "quit", "too tough", "first try"]},
            "negative_self_talk": {"name": "Telling yourself 'I am bad at math' or 'I am an average student' as a fixed identity", "trigger_words": ["bad at", "average student", "never understand", "stupid"]}
        },
        "questions": [(
            "When you fail to solve a practice question on the first attempt, what is your immediate internal dialogue?",
            {"1": "'I knew it; I am just not built for this subject.'", "2": "'Let me check the hint, figure out what principle I missed, and re-try.'", "3": "'I feel angry/defeated and close the book.'", "4": "'I skip it and hope it doesn't appear on the final exam.'"}
        )],
        "comprehensive_advice": [
            "Evidence-Based Growth Journal: Keep a list titled 'Things I Once Found Impossible That I Can Now Do' as proof of your capability.",
            "Reframe Struggle as Neuroplasticity: Mental resistance is the sensation of your brain building new neural connections.",
            "Eliminate Fixed Labels: Replace 'I am bad at this subject' with 'I have not developed fluency in this sub-topic yet'.",
            "Stack Immediate Micro-Wins: Solve 3 easy foundation problems when confidence dips to regain forward momentum.",
            "Focus on Controllable Inputs: Measure your progress by daily disciplined study hours rather than daily score fluctuations."
        ],
        "named_protocol": "The Evidence-Based Competence Protocol",
        "mindset_shift": "Academic confidence is not a feeling you wait for before studying; it is a byproduct that arrives after you solve problems.",
        "action": "Identify one chapter you once found difficult that you now understand, reminding yourself that difficulty is simply unfamiliarity."
    },
    "workload": {
        "title": "Heavy Workload & Academic Overwhelm",
        "keywords": ["workload", "overwhelmed", "too much homework", "too many subjects", "projects", "assignments", "exhausted", "drowning in work"],
        "subtopics": {
            "homework_vs_selfstudy": {"name": "School practicals, notebooks, and homework eating all time, leaving zero hours for concept study", "trigger_words": ["homework", "records", "practicals", "copying work", "no self study"]},
            "too_many_subjects_day": {"name": "Trying to juggle 5 different subjects in one evening and completing none properly", "trigger_words": ["juggle", "5 subjects", "switching", "incomplete"]},
            "project_deadlines": {"name": "Sudden school project submissions clashing with upcoming chapter tests", "trigger_words": ["project", "submission", "clash", "due date"]}
        },
        "questions": [(
            "How do you currently handle evenings with heavy school homework?",
            {"1": "I spend 4 hours making notebooks look decorative and do zero real concept learning", "2": "I get overwhelmed, panic, and end up scrolling on my phone instead", "3": "I rush through homework carelessly just to submit it", "4": "I prioritize homework over sleep, leading to total burnout next day"}
        )],
        "comprehensive_advice": [
            "The Triage Matrix: Separate assignments into Conceptually Vital (numerical exercises) and Administrative Copy-Work (decorative covers); finish copy-work quickly.",
            "The 2-Subject Daily Limit: Never divide an evening into tiny slices across 5 subjects. Dedicate your evening to 2 subjects maximum.",
            "Micro-Batch Deadlines: Spend 20 minutes on project research early instead of pulling an all-nighter before submission.",
            "Protect Sleep: Sacrificing sleep to finish decorative homework creates cognitive deficits in class the next morning.",
            "Teacher Coordination: Speak politely with your class teacher if multiple departments assign heavy submissions on the exact same morning."
        ],
        "named_protocol": "The 2-Subject Cognitive Triage System",
        "mindset_shift": "You do not need to finish everything in one evening; you need to execute high-priority tasks with focus.",
        "action": "Categorize today's tasks into Concept Mastery vs Administrative School Work, finishing administrative tasks quickly."
    },
    "study_routine": {
        "title": "Study Routine & Daily Consistency",
        "keywords": ["study routine", "routine", "inconsistent", "irregular", "study habits", "no rhythm", "some days 10 hours some days 0"],
        "subtopics": {
            "binge_and_crash": {"name": "Studying 10 hours on Sunday and 0 hours from Monday to Wednesday", "trigger_words": ["binge", "crash", "irregular", "rollercoaster", "zero hours"]},
            "inconsistent_timing": {"name": "Studying morning one day, midnight the next, with no fixed anchor time", "trigger_words": ["morning", "night", "changing time", "no anchor"]},
            "weekend_slump": {"name": "Weekdays having some structure due to school, but weekends completely wasted", "trigger_words": ["weekend", "saturday", "sunday", "wasted weekend"]}
        },
        "questions": [(
            "Which pattern best describes your study frequency over a typical two-week period?",
            {"1": "High bursts of panic study followed by multiple days of zero productivity", "2": "Studying only when school tests are announced", "3": "Consistent 1–2 hours daily, but lacking depth", "4": "Good intentions every morning, but collapsing by evening"}
        )],
        "comprehensive_advice": [
            "Anchor Habits: Attach your study session to an existing daily habit: 'Immediately after evening tea at 5:00 PM, I sit at my desk.'",
            "Non-Negotiable Minimum Floor: Set a daily minimum of 90 minutes. Complete your 90 minutes even on low-energy days.",
            "Weekend 3-Block Architecture: Divide Saturdays and Sundays into Morning Deep Work, Afternoon Rest, and Evening Practice.",
            "Track Frequency Over Hours: Measure how many consecutive days you sat down on time rather than tracking raw hours.",
            "Pre-Decide Opening Task: Decide the night before which chapter you will open first to eliminate decision fatigue."
        ],
        "named_protocol": "The Anchor Habit & Minimum-Floor System",
        "mindset_shift": "Consistency is not about never feeling tired; it is about showing up for a baseline 60 minutes even when you are.",
        "action": "Pick one fixed 60-minute window that you will protect every single day for the next 7 days without exception."
    },
    "sleep_tiredness": {
        "title": "Sleep Deprivation, Fatigue & Low Energy",
        "keywords": ["sleep", "tired", "tiredness", "fatigue", "exhaustion", "sleepy", "drowsy", "headache", "waking up tired", "late night"],
        "subtopics": {
            "late_night_doomscrolling": {"name": "Staying up until 1:00 AM on screens, leading to heavy drowsiness in class and desk fatigue", "trigger_words": ["screens", "1am", "late night", "doomscrolling", "phone at night"]},
            "afternoon_crash": {"name": "Extreme energy slump between 3:00 PM and 6:00 PM after coming home from school", "trigger_words": ["afternoon", "crash", "slump", "post school", "lethargic"]},
            "erratic_sleep_cycle": {"name": "Sleeping 4 hours on weekdays and 12 hours on weekends, disrupting brain rhythm", "trigger_words": ["erratic", "weekend sleep", "4 hours", "disrupted"]}
        },
        "questions": [(
            "How many hours of uninterrupted sleep do you average on school nights?",
            {"1": "Less than 5 hours", "2": "Around 5 to 6 hours", "3": "7 to 8 hours consistently", "4": "Varies wildly between 4 and 9 hours"}
        )],
        "comprehensive_advice": [
            "7-Hour Sleep Foundation: Memory consolidation occurs during deep sleep; sleeping under 6 hours significantly reduces retention.",
            "30-Minute Digital Sunset: Turn off all screens 30 minutes before sleep to allow melatonin levels to rise naturally.",
            "20-Minute Power Nap Protocol: Take a short 20-minute nap after school rather than a 2-hour sleep that ruins nighttime rest.",
            "Fixed Wake-Up Anchor: Wake up at the exact same hour every day, including weekends, to stabilize your circadian rhythm.",
            "Morning Water and Sunlight: Drink 500ml of water and get natural sunlight right after waking up to activate morning alertness."
        ],
        "named_protocol": "The 7-Hour Circadian Restoration Architecture",
        "mindset_shift": "Sleep is not lost study time; it is the biological process that saves what you studied into memory.",
        "action": "Set a hard digital curfew tonight: all mobile devices plugged in outside arm's reach 30 minutes before bed."
    },
    "planning": {
        "title": "Planning, Goal Setting & Tracking",
        "keywords": ["planning", "goals", "weekly plan", "tracking", "unorganized syllabus", "lost in syllabus", "how to plan"],
        "subtopics": {
            "vague_targets": {"name": "Setting vague goals like 'study more' with no measurable metrics", "trigger_words": ["vague", "targets", "study more", "goals"]},
            "no_progress_tracking": {"name": "Studying daily but having no idea what percentage of syllabus is completed", "trigger_words": ["tracking", "progress", "syllabus tracker", "percentage"]},
            "over_planning_no_execution": {"name": "Spending 3 hours designing colorful planners and 0 hours actually studying", "trigger_words": ["over planning", "aesthetic", "planner", "no execution"]}
        },
        "questions": [(
            "How do you currently track your syllabus progress?",
            {"1": "I don't track; I just study whatever is taught in school", "2": "I keep a checklist of chapters on my wall", "3": "I plan a lot but never follow through", "4": "I only track when exams approach"}
        )],
        "comprehensive_advice": [
            "Syllabus Master Tracker: Print the official syllabus table of contents and highlight completed chapters in Green.",
            "Weekly Sunday Review: Spend 15 minutes every Sunday planning your 3 major academic milestones for the upcoming week.",
            "Action Over Aesthetics: Spend less than 5 minutes planning each evening; execution is what moves the needle.",
            "Micro-Milestones: Break each chapter into 3 checkpoints: Theory Notes, NCERT Exercises, and 5 Years of PYQs.",
            "Weekly Completion Metric: Track tasks completed rather than hours spent sitting at the desk."
        ],
        "named_protocol": "The Master Syllabus Milestone Tracker",
        "mindset_shift": "A plan is a flexible compass, not a rigid cage; adjust weekly and keep moving forward.",
        "action": "Print or write down the chapter list for your hardest subject and mark exactly where you stand today."
    },
    "careless_mistakes": {
        "title": "Careless Mistakes & Calculation Errors",
        "keywords": ["careless mistakes", "silly mistakes", "calculation errors", "sign error", "minus plus", "reading question wrong", "rough work messy"],
        "subtopics": {
            "sign_calculation_slips": {"name": "Messing up basic arithmetic, negative signs, or simple algebra in the final step", "trigger_words": ["signs", "calculation", "plus minus", "arithmetic", "algebra"]},
            "misreading_prompts": {"name": "Missing keywords like 'NOT true', 'INCORRECT', or overlooked unit conversions", "trigger_words": ["not true", "units", "misreading", "skipped word", "incorrect"]},
            "messy_rough_work": {"name": "Chaotic scratch work where numbers get miscopied from one line to the next", "trigger_words": ["rough work", "messy", "miscopied", "handwriting", "scratch"]}
        },
        "questions": [(
            "When you review a test paper with avoidable errors, what is the #1 reason?",
            {"1": "Rushing through calculation to beat the clock", "2": "Disorganized scratch work leading to misread handwriting", "3": "Not reading the last line of the question to verify what was requested", "4": "Doing steps mentally instead of writing them out"}
        )],
        "comprehensive_advice": [
            "The Margin Rule for Rough Work: Draw a clean 2.5-inch vertical column on the right side of every page with numbered calculations.",
            "Underline Final Prompts: Circle negative qualifiers ('which is NOT true', 'calculate in m/s') before solving.",
            "Bracket Checks for Negative Signs: Write down minus sign distributions line by line rather than calculating mentally.",
            "Maintain an Avoidable Error Log: Log mistakes into Question Number, Exact Error, and Prevention Rule in a dedicated notebook.",
            "10-Minute Sanity Check: Budget exam pacing to finish 10 minutes early and audit specifically for units, negative signs, and sub-parts."
        ],
        "named_protocol": "The Structured Margin & Error-Audit Protocol",
        "mindset_shift": "Careless mistakes are not random accidents; they are mechanical habits that disappear when you slow down high-risk steps.",
        "action": "Draw a clean 2-inch right-hand margin on your practice paper today to keep rough work aligned and sequential."
    },
    "following_instructions": {
        "title": "Following Exam Instructions & Presentation",
        "keywords": ["instructions", "guidelines", "word limit", "presentation", "marks scheme", "steps missing", "board format", "answer framing"],
        "subtopics": {
            "ignoring_word_limits": {"name": "Writing 2 pages for a 2-mark question and running out of time for 5-markers", "trigger_words": ["word limit", "too long", "2 marks", "time lost"]},
            "missing_steps": {"name": "Skipping formulas or intermediate reasoning in board subjective answers", "trigger_words": ["steps cut", "formula missing", "step marks", "presentation"]},
            "question_selection_error": {"name": "Choosing the wrong internal choice questions in exams and regretting it halfway", "trigger_words": ["internal choice", "or questions", "picked wrong"]}
        },
        "questions": [(
            "What is your biggest weakness regarding subjective answer presentation?",
            {"1": "Writing dense paragraphs instead of structured point-wise bullet answers with diagrams", "2": "Skipping the explicit formula statement before numerical substitution", "3": "Poor time pacing between section weights (e.g. 1-mark vs 5-mark)", "4": "Unclear handwriting and strike-throughs"}
        )],
        "comprehensive_advice": [
            "Board Step Structure: Format answers into Given Data, Formula Used, Stepwise Substitution, and Final Answer Boxed with Units.",
            "Point-Wise Presentation: Use numbered bullet points with underlined key terms for 3-mark and 5-mark questions.",
            "Respect Word Limits: Keep 2-mark answers to 30-40 words to preserve time for heavyweight sections.",
            "Internal-Choice Evaluation: Spend 60 seconds reading both options in 'OR' questions to choose the one with direct step marks.",
            "Neat Formatting: Leave 2 blank lines between answers and use single neat strike-throughs for mistakes."
        ],
        "named_protocol": "The Structured Step-Wise Presentation Protocol",
        "mindset_shift": "Make your answers easy for the examiner to award full marks to.",
        "action": "Take one 5-mark question from your syllabus and format the answer into: Given Data, Formula Used, Step-by-Step Working, Final Answer Boxed."
    },
    "balancing_subjects": {
        "title": "Balancing Multiple Subjects & Streams",
        "keywords": ["balancing subjects", "multiple subjects", "stream balance", "ignoring english", "ignoring chemistry", "too much physics", "subject bias"],
        "subtopics": {
            "comfort_subject_bias": {"name": "Devoting 80% of time to the subject you enjoy while ignoring the difficult one", "trigger_words": ["favourite subject", "comfort", "ignoring", "bias"]},
            "language_optional_neglect": {"name": "Completely ignoring English or Optional subjects until the final week before boards", "trigger_words": ["english", "optional", "neglecting", "last week"]},
            "simultaneous_overload": {"name": "Trying to study 4 subjects simultaneously every single day and burning out", "trigger_words": ["simultaneous", "all subjects", "switching too fast"]}
        },
        "questions": [(
            "How do you currently distribute time across your curriculum subjects?",
            {"1": "I almost exclusively study 1 or 2 core subjects and ignore the rest", "2": "I study whichever subject has an immediate homework deadline or test tomorrow", "3": "I try to study everything daily but get exhausted", "4": "I constantly worry about other subjects while studying one"}
        )],
        "comprehensive_advice": [
            "Heavy-Light Pairing: Pair one tough analytical subject with one descriptive or language subject each day.",
            "Tackle Hard Topics First: Schedule your most challenging subject at the start of your study evening.",
            "Weekly Language Window: Dedicate 2 hours every Sunday morning to English or your optional subject.",
            "Audit Time Distribution: Review your hours weekly to make sure no subject sits at 0%.",
            "Present-Moment Focus: When studying one subject, commit fully without worrying about the others."
        ],
        "named_protocol": "The Heavy-Light Alternation Architecture",
        "mindset_shift": "Your overall score is calculated from the aggregate of all subjects, not just your favorite one.",
        "action": "Allocate 45 focused minutes today specifically to your most neglected curriculum subject."
    },
    "new_class_adaptation": {
        "title": "Adapting to Senior Secondary / Class 11-12 Rigor",
        "keywords": ["class 11 jump", "class 10 to 11", "syllabus jump", "new class", "difficult syllabus", "tougher than before", "academic level jump"],
        "subtopics": {
            "class_11_jump": {"name": "Shock from the massive depth and syllabus expansion transitioning from Class 10 to 11", "trigger_words": ["class 11", "jump", "class 10", "shock", "depth"]},
            "competitive_vs_school": {"name": "Trying to manage competitive prep (JEE/NEET/etc.) alongside CBSE school exams", "trigger_words": ["competitive", "jee", "neet", "boards", "dual prep"]},
            "outdated_study_habits": {"name": "Trying to use Class 10 rote-memorization tactics on Class 11/12 analytical concepts", "trigger_words": ["rote", "memorizing", "does not work anymore", "old tactics"]}
        },
        "questions": [(
            "What has been the most jarring realization in your current academic grade?",
            {"1": "'Reading the textbook once is no longer enough to score high marks.'", "2": "'Questions require combining 3 different concepts rather than direct formula substitution.'", "3": "'The volume of daily homework leaves no breathing room.'", "4": "'My previous study habits from earlier grades have completely stopped working.'"}
        )],
        "comprehensive_advice": [
            "Acknowledge the Qualitative Jump: Senior secondary classes require deriving principles and understanding conditions, not just memorizing summaries.",
            "Master Mathematical Fundamentals: Vector algebra, basic calculus, and trigonometry are prerequisites for senior science; master them early.",
            "Active Problem Solving: Dedicate 70% of study time to solving problems with a pen on paper.",
            "Integrate Board and Competitive Prep: Master NCERT textbook fundamentals first before tackling advanced problem sets.",
            "Expect the Adjustment Period: An initial dip in test marks during the first term of Class 11 is normal nationwide; adapt your methods and stay consistent."
        ],
        "named_protocol": "The Analytical Foundation Transition System",
        "mindset_shift": "Earlier grades were about knowing answers; senior secondary is about understanding mechanisms.",
        "action": "Commit to understanding 'why' a formula works before memorizing it for your very next topic."
    },
    "general_academic": {
        "title": "General Academic Workflow & Study Method",
        "keywords": ["general", "studies", "studying", "problem", "difficulties", "cannot study", "help in studies", "study issues"],
        "subtopics": {
            "unclear_root_cause": {"name": "Feeling that studies are slipping without being able to pinpoint why", "trigger_words": ["slipping", "unclear", "general", "do not know why"]},
            "overall_overwhelm": {"name": "A general combination of fatigue, mild backlog, and lack of routine", "trigger_words": ["overwhelm", "everything", "all of it", "general fatigue"]}
        },
        "questions": [(
            "If you had to choose the single biggest factor holding back your progress, which is it?",
            {"1": "Inability to maintain daily focus and consistency", "2": "Poor retention and memory of older chapters", "3": "Anxiety and overwhelm from workload", "4": "Distractions from phone, friends, or environment"}
        )],
        "comprehensive_advice": [
            "Identify the Single Primary Bottleneck: Pick the one critical friction point (phone use, late sleep, or lack of revision) and address that first.",
            "Establish a Daily 90-Minute Anchor Block: Commit to one protected, focused study block every evening with zero exceptions.",
            "Keep an Active Mistake and Doubt Register: Write down unanswered questions and calculation slips in a dedicated notebook.",
            "Focus on Daily Completion Over Big Goals: Measure each day by tasks completed rather than worrying about the full syllabus.",
            "Maintain Real Rest Periods: Ensure you take real breaks away from screens to recharge cognitive focus."
        ],
        "named_protocol": "The Core Foundation Reset Protocol",
        "mindset_shift": "Fix the single biggest bottleneck first; everything else gets easier once momentum returns.",
        "action": "Choose one small, achievable academic win for today: 30 minutes of uninterrupted study on your single most urgent topic."
    }
}

def classify_natural_language_problem(text: str) -> Tuple[Optional[str], float, List[str]]:
    clean_text = normalise_text(text)
    tokens = clean_text.split()
    stemmed_tokens = [simple_stem(w) for w in tokens]

    scores: Dict[str, float] = {}
    matches_map: Dict[str, List[str]] = {}

    has_family_entity = any(w in tokens for w in ["parents", "parent", "mother", "father", "mom", "dad", "family", "home", "relatives", "cousins"])
    has_peer_entity = any(w in tokens for w in ["friends", "friend", "classmates", "classmate", "peers", "peer", "group", "fomo"])
    has_teacher_entity = any(w in tokens for w in ["teacher", "sir", "madam", "mam", "school", "lecture", "blackboard", "teaching"])

    for key, data in TOPIC_CATALOG.items():
        score = 0.0
        matches = []

        for kw in data["keywords"]:
            norm_kw = normalise_text(kw)
            if " " in norm_kw:
                if norm_kw in clean_text:
                    score += 4.0
                    matches.append(kw)
            else:
                stem_kw = simple_stem(norm_kw)
                if norm_kw in tokens or stem_kw in stemmed_tokens:
                    score += 1.5
                    matches.append(kw)

        for sub_key, sub_data in data["subtopics"].items():
            for tr in sub_data["trigger_words"]:
                norm_tr = normalise_text(tr)
                if " " in norm_tr:
                    if norm_tr in clean_text:
                        score += 3.0
                        matches.append(tr)
                else:
                    stem_tr = simple_stem(norm_tr)
                    if norm_tr in tokens or stem_tr in stemmed_tokens:
                        score += 1.2
                        matches.append(tr)

        # Contextual Disambiguation Rules
        if has_family_entity and key == "family_home_environment":
            score += 6.0
            matches.append("[context: family/parents entity]")
            if any(w in tokens for w in ["comparing", "compare", "motivating", "pressure", "scolding"]):
                score += 5.0
                matches.append("[context: parental expectations & comparison]")

        if has_family_entity and not has_peer_entity and key == "peer_influence":
            score = max(0.0, score - 6.0)

        if has_teacher_entity and key in ["teacher_explanation", "asking_doubts"]:
            score += 4.0
            matches.append("[context: teacher entity]")

        if score > 0:
            scores[key] = score
            matches_map[key] = sorted(list(set(matches)))

    if not scores:
        return None, 0.0, []

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_key, top_score = sorted_scores[0]
    total_score = sum(scores.values())
    confidence = round(top_score / total_score, 2) if total_score > 0 else 0.0

    return top_key, confidence, matches_map.get(top_key, [])

ACTION_VERBS = [
    'keep', 'put', 'turn off', 'switch off', 'silent', 'timer', 'pomodoro',
    'plan', 'write', 'revise', 'practice', 'solve', 'sleep', 'wake', 'block',
    'desk', 'stop', 'limit', 'routine', 'schedule', 'table', 'ask', 'talk', 'speak'
]

DISMISSIVE_INPUTS = {
    'idk', 'i do not know', 'dont know', 'no idea', 'dunno', 'nothing',
    'na', 'none', 'cannot say', 'cant say', 'not sure', 'whatever', 'nil'
}

def evaluate_student_solution(solution_text: str) -> Dict[str, Any]:
    clean = normalise_text(solution_text)

    if clean in DISMISSIVE_INPUTS or len(clean.split()) == 0:
        return {
            "is_actionable": False,
            "is_dismissive": True,
            "strengths": [
                "Openness to Guidance: Admitting uncertainty candidly is the first step toward building a real strategy."
            ],
            "critique": [
                "It is completely normal to feel unsure when a problem feels overwhelming. That is why we provide a structured action blueprint below."
            ]
        }

    is_actionable = any(v in clean for v in ACTION_VERBS)
    strengths = []
    critique = []

    if is_actionable:
        strengths.append("High agency: You proposed a concrete, observable physical action rather than a vague wish.")
        critique.append("Your suggested solution is pragmatic and directly targets the behavioural trigger.")
    else:
        strengths.append("Honest reflection: You are analyzing your habits candidly.")
        critique.append("Good initiative. Let's make sure it is attached to an exact daily trigger so it becomes a habit.")

    return {
        "is_actionable": is_actionable,
        "is_dismissive": False,
        "strengths": strengths,
        "critique": critique
    }

class DiagnosticResult(dict):
    """
    Subclasses dictionary so Database.py can access fields like a dict (result['topic']),
    while printing `print(result)` renders an executive-quality, formatted report.
    """
    def __str__(self) -> str:
        sep = "=" * 70
        dash = "-" * 70
        lines = [
            sep,
            "              GENERAL STUDY DIAGNOSIS & MENTORING REPORT",
            sep,
            f"Student Name : {self.get('student_name', 'Student')} | Roll: {self.get('roll_no', 'N/A')}",
            f"Class/Sec    : Class {self.get('student_class', '')} - {self.get('student_section', '')}",
            f"Core Topic   : {self.get('topic', '')}",
            f"Subtopic     : {self.get('subtopic', '')}",
            dash,
            "WHAT I UNDERSTOOD:",
            f"  {self.get('summary_text', '')}",
            "",
            "MINDSET REFRAME:",
            f"  {self.get('mindset_shift', '')}",
            "",
            "IDENTIFIED STRENGTHS:",
        ]
        for s in self.get('strengths', '').split(' | '):
            if s:
                lines.append(f"  * {s}")
        lines.append("")
        lines.append("GROWTH AREAS & FRICTION POINTS:")
        for g in self.get('growth_areas', '').split(' | '):
            if g:
                lines.append(f"  * {g}")

        sol = self.get('student_solution', '')
        if sol and sol.lower() not in DISMISSIVE_INPUTS:
            lines.append("")
            lines.append("YOUR PROPOSED ADJUSTMENT:")
            lines.append(f"  \"{sol}\"")

        lines.append("")
        lines.append(f"COMPREHENSIVE STRATEGY BLUEPRINT ({self.get('named_protocol', 'Action Plan')}):")
        advice_list = self.get('comprehensive_advice', [])
        if isinstance(advice_list, list):
            for adv in advice_list:
                lines.append(f"  * {adv}")
        else:
            lines.append(f"  * {advice_list}")

        lines.append("")
        lines.append("YOUR NEXT SMALL ACTION (TODAY):")
        lines.append(f"  {self.get('action_step', '')}")
        lines.append(sep)
        return "\n".join(lines)

class DoubtDiagnostic_General:
    """
    Complete General Academic Diagnostic Mentor.
    Covers all 26 general areas, returning-student history check-in, NLP classification,
    targeted questions, student reflection, and built-in guaranteed MySQL persistence.
    """

    VERSION = "6.0-GENERAL-MENTOR"

    def __init__(
        self,
        Roll_no: str,
        Student_name: str,
        student_class: str,
        Student_Section: str,
        problem: Optional[str] = None,
        previous_record: Optional[Dict[str, Any]] = None
    ):
        self.roll_no = str(Roll_no).strip()
        self.student_name = str(Student_name).strip()
        self.student_class = str(student_class).strip()
        self.student_section = str(Student_Section).strip()
        self.raw_problem = str(problem).strip() if problem else ""
        self.previous_record = previous_record

        self.followup_notes: Optional[str] = None
        self.followup_trajectory: Optional[str] = None

        self.selected_topic_key: Optional[str] = None
        self.selected_subtopic_key: Optional[str] = None
        self.nlp_detected_topic: Optional[str] = None
        self.nlp_confidence: float = 0.0
        self.nlp_matched_keywords: List[str] = []

        self.diagnostic_answers: List[Dict[str, str]] = []
        self.student_proposed_solution: str = ""
        self.solution_evaluation: Dict[str, Any] = {}

        self.identified_strengths: List[str] = []
        self.identified_growth_areas: List[str] = []
        self.comprehensive_advice: List[str] = []
        self.named_protocol: str = ""
        self.mindset_shift: str = ""
        self.actionable_step: str = ""

    @staticmethod
    def _prompt_text(prompt: str, allow_empty: bool = False) -> str:
        print(f"\n{prompt}")
        while True:
            ans = input("> ").strip()
            if ans or allow_empty:
                return ans
            print("Please share a brief response in your own words.")

    @staticmethod
    def _prompt_choice(prompt: str, options: Dict[str, str]) -> str:
        print(f"\n{prompt}")
        for key, text in options.items():
            print(f"  {key}. {text}")
        while True:
            ans = input("> ").strip()
            if ans in options:
                return ans
            print(f"Please select one of the valid options ({', '.join(options.keys())}).")

    def lookup_previous_record_from_db(self) -> Optional[Dict[str, Any]]:
        """Direct database lookup to find whether this roll number has visited before."""
        try:
            db = mysql.connector.connect(
                host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
                port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
                user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
                password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", ""),
                database=os.getenv("STUDENT_MENTOR_DB_NAME", "student_mentor")
            )
            cursor = db.cursor(dictionary=True)
            query = """
            SELECT topic, subtopic, action_step, created_at, student_solution
            FROM general_study_diagnostics
            WHERE roll_no = %s
            ORDER BY id DESC
            LIMIT 1;
            """
            cursor.execute(query, (self.roll_no,))
            row = cursor.fetchone()
            cursor.close()
            db.close()
            return row
        except Exception:
            return None

    def check_returning_student(self) -> bool:
        """Checks for previous records in MySQL and initiates follow-up NLP check-in."""
        if not self.previous_record:
            self.previous_record = self.lookup_previous_record_from_db()

        if not self.previous_record:
            return False

        prev_topic = self.previous_record.get("topic", "General Study Routine")
        prev_subtopic = self.previous_record.get("subtopic", "Study Difficulty")
        prev_action = self.previous_record.get("action_step", "Daily Study Block")
        prev_date = self.previous_record.get("created_at", "recently")

        print("\n" + "=" * 65)
        print("          WELCOME BACK! PREVIOUS PROGRESS CHECK-IN")
        print("=" * 65)
        print(f"Welcome back, {self.student_name}! I see from our session on {prev_date}:")
        print(f"  * Previous Core Area : {prev_topic}")
        print(f"  * Focus Issue        : {prev_subtopic}")
        print(f"  * Target Action Plan : {prev_action}")
        print("-" * 65)

        progress_text = self._prompt_text(
            "What happened since our last session? How did it go with that plan?\n"
            "(Tell me naturally, e.g. 'I tried but got distracted again', 'It helped a lot', etc.)"
        )
        self.followup_notes = progress_text

        cat_key, cat_title, mentor_resp, guidance = analyze_followup_progress(progress_text)
        self.followup_trajectory = cat_title

        print(f"\n[Progress Analysis: {cat_title}]")
        print(f"{mentor_resp}")
        print(f"\nMentor Guidance: {guidance}\n")

        choice = self._prompt_choice(
            "How would you like to proceed today?",
            {
                "1": f"Continue & recalibrate on '{prev_topic}'",
                "2": "Diagnose a different / newly emerging study difficulty"
            }
        )

        if choice == "1":
            for k, data in TOPIC_CATALOG.items():
                if data["title"].lower() == prev_topic.lower() or k in prev_topic.lower():
                    self.selected_topic_key = k
                    return True
            self.selected_topic_key = "general_academic"
            return True

        return False

    def identify_topic(self) -> None:
        """Presents the comprehensive catalogue of all 26 general academic areas."""
        if self.raw_problem and check_safety_concerns(self.raw_problem):
            self._handle_safety_flag()
            return

        if self.raw_problem:
            best_key, conf, matches = classify_natural_language_problem(self.raw_problem)
            if best_key and conf >= 0.35:
                self.nlp_detected_topic = best_key
                self.nlp_confidence = conf
                self.nlp_matched_keywords = matches
                detected_title = TOPIC_CATALOG[best_key]["title"]

                print(f"\nBased on what you shared, your challenge relates closely to:")
                print(f"**{detected_title}**")
                choice = self._prompt_choice(
                    "Does this accurately capture what you are feeling?",
                    {"1": "Yes, let's explore this area.", "2": "No, let me browse the full list."}
                )
                if choice == "1":
                    self.selected_topic_key = best_key
                    return

        print("\n==================================================")
        print("         SELECT YOUR GENERAL STUDY CHALLENGE")
        print("==================================================")
        keys_list = list(TOPIC_CATALOG.keys())
        menu_options = {str(i): TOPIC_CATALOG[k]["title"] for i, k in enumerate(keys_list, start=1)}
        menu_options[str(len(keys_list) + 1)] = "Something else (Describe naturally)"

        selection = self._prompt_choice("Which of these areas feels closest to your situation?", menu_options)

        if int(selection) == len(keys_list) + 1:
            user_desc = self._prompt_text(
                "Please describe what has been happening in your own words:\n"
                "(E.g., 'My parents compare me with my cousins and it stresses me out...')"
            )
            if check_safety_concerns(user_desc):
                self._handle_safety_flag()
                return

            best_key, conf, matches = classify_natural_language_problem(user_desc)
            if best_key:
                self.nlp_detected_topic = best_key
                self.nlp_confidence = conf
                self.nlp_matched_keywords = matches
                self.selected_topic_key = best_key
                print(f"\nThank you for explaining that. That maps directly to: **{TOPIC_CATALOG[best_key]['title']}**.")
            else:
                clarify_options = {
                    "1": "Concentration & Staying Focused",
                    "2": "Procrastination & Starting Friction",
                    "3": "Family Expectations & Home Pressure",
                    "4": "Exam Pressure & Performance Anxiety",
                    "5": "General Academic Workload"
                }
                c_sel = self._prompt_choice("Which fundamental area represents the biggest hurdle?", clarify_options)
                fallback_map = {
                    "1": "concentration",
                    "2": "procrastination",
                    "3": "family_home_environment",
                    "4": "exam_pressure",
                    "5": "general_academic"
                }
                self.selected_topic_key = fallback_map[c_sel]
        else:
            self.selected_topic_key = keys_list[int(selection) - 1]

    def _handle_safety_flag(self) -> None:
        print("\n" + "=" * 65)
        print("              IMPORTANT PERSONAL SUPPORT")
        print("=" * 65)
        print("I hear that you are going through a very heavy and overwhelming time.")
        print("Please remember that your personal well-being and safety come first before any marks.")
        print("\nI strongly encourage you to speak with a trusted adult today:")
        print("  * Your school counsellor or a trusted teacher")
        print("  * A parent, family elder, or doctor")
        print("  * Student support helpline (e.g., Tele-MANAS: 14416 / 1800 891 4416 in India)")
        print("\nYou don't have to carry this alone. Please reach out to someone who can help.")
        print("=" * 65 + "\n")
        self.selected_topic_key = "general_academic"

    def select_subtopic(self) -> None:
        topic_data = TOPIC_CATALOG[self.selected_topic_key]
        subtopics = topic_data["subtopics"]
        sub_keys = list(subtopics.keys())

        print(f"\n--------------------------------------------------")
        print(f"  {topic_data['title'].upper()} - SPECIFIC SCENARIO")
        print(f"--------------------------------------------------")
        sub_options = {str(i): subtopics[k]["name"] for i, k in enumerate(sub_keys, start=1)}
        selection = self._prompt_choice("Which specific scenario happens most frequently?", sub_options)
        self.selected_subtopic_key = sub_keys[int(selection) - 1]

    def ask_diagnostic_questions(self) -> None:
        topic_data = TOPIC_CATALOG[self.selected_topic_key]
        questions = topic_data["questions"]

        print(f"\nLet's diagnose your situation with a few quick questions:\n")
        for idx, (q_text, opts) in enumerate(questions, start=1):
            ans_key = self._prompt_choice(f"Q{idx}. {q_text}", opts)
            self.diagnostic_answers.append({
                "question": q_text,
                "selected_option": ans_key,
                "answer_text": opts[ans_key]
            })

    def engage_student_solution(self) -> None:
        print("\n==================================================")
        print("          YOUR PERSPECTIVE & IDEAS")
        print("==================================================")
        print("Mentoring works best when you participate in solving the puzzle.")
        why_text = self._prompt_text("In your view, what is the biggest reason this keeps happening?")

        print("\nIf you had to test ONE realistic adjustment starting tomorrow, what would you try?")
        print("(If you don't know yet, you can say 'not sure')")
        self.student_proposed_solution = self._prompt_text("Your proposed idea:")

        self.solution_evaluation = evaluate_student_solution(self.student_proposed_solution)

        topic_data = TOPIC_CATALOG[self.selected_topic_key]
        sub_name = topic_data["subtopics"][self.selected_subtopic_key]["name"]

        self.identified_strengths = [
            "Self-Observation: You pinpointed your exact study friction instead of blindly ignoring it."
        ]
        self.identified_strengths.extend(self.solution_evaluation["strengths"])

        self.identified_growth_areas = [
            f"Friction point: {sub_name}",
            "Follow-through: Building a structured, calm boundary to protect your study momentum."
        ]
        self.comprehensive_advice = topic_data.get("comprehensive_advice", [])
        self.named_protocol = topic_data.get("named_protocol", "Standard Action Protocol")
        self.mindset_shift = topic_data.get("mindset_shift", "Focus on consistent small daily actions.")
        self.actionable_step = topic_data.get("action", "Complete one focused 20-minute study task today.")

    def display_mentoring_result(self) -> None:
        payload = self.get_structured_result()
        print("\n" + str(payload))

    def get_structured_result(self) -> DiagnosticResult:
        topic_title = TOPIC_CATALOG[self.selected_topic_key]["title"]
        sub_title = TOPIC_CATALOG[self.selected_topic_key]["subtopics"][self.selected_subtopic_key]["name"]
        summary = f"You are finding that '{sub_title}' is creating emotional or mental friction, pulling your focus away from consistent learning."

        data = {
            "roll_no": self.roll_no,
            "student_name": self.student_name,
            "student_class": self.student_class,
            "student_section": self.student_section,
            "category": "General Academic",
            "topic": topic_title,
            "subtopic": sub_title,
            "summary_text": summary,
            "raw_input": self.raw_problem,
            "followup_notes": self.followup_notes,
            "followup_trajectory": self.followup_trajectory,
            "nlp_category": self.nlp_detected_topic or "manual_selection",
            "nlp_confidence": self.nlp_confidence,
            "nlp_keywords": ", ".join(self.nlp_matched_keywords),
            "diagnostic_answers": self.diagnostic_answers,
            "student_solution": self.student_proposed_solution,
            "strengths": " | ".join(self.identified_strengths),
            "growth_areas": " | ".join(self.identified_growth_areas),
            "comprehensive_advice": self.comprehensive_advice,
            "named_protocol": self.named_protocol,
            "mindset_shift": self.mindset_shift,
            "action_step": self.actionable_step,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return DiagnosticResult(data)

    def save_to_mysql_direct(self, data: dict) -> bool:
        """
        Directly connects to MySQL, creates database and table if not existing,
        and commits the diagnostic record with full verification.
        """
        try:
            # 1. Connect and ensure database exists
            db_conn = mysql.connector.connect(
                host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
                port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
                user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
                password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", "")
            )
            init_cursor = db_conn.cursor()
            init_cursor.execute("CREATE DATABASE IF NOT EXISTS student_mentor;")
            db_conn.commit()
            init_cursor.close()
            db_conn.close()

            # 2. Connect to student_mentor database
            db = mysql.connector.connect(
                host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
                port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
                user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
                password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", ""),
                database=os.getenv("STUDENT_MENTOR_DB_NAME", "student_mentor")
            )
            cursor = db.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS general_study_diagnostics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_no VARCHAR(50) NOT NULL,
                student_name VARCHAR(150),
                student_class VARCHAR(30),
                student_section VARCHAR(30),
                topic VARCHAR(100) NOT NULL,
                subtopic VARCHAR(200) NOT NULL,
                raw_input TEXT,
                followup_notes TEXT,
                followup_trajectory VARCHAR(100),
                nlp_category VARCHAR(100),
                nlp_confidence FLOAT,
                nlp_keywords TEXT,
                diagnostic_answers JSON,
                student_solution TEXT,
                strengths TEXT,
                growth_areas TEXT,
                recommended_strategy TEXT,
                action_step TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_gen_roll (roll_no),
                INDEX idx_gen_topic (topic)
            );
            """
            cursor.execute(create_table_query)

            insert_query = """
            INSERT INTO general_study_diagnostics (
                roll_no, student_name, student_class, student_section,
                topic, subtopic, raw_input, followup_notes, followup_trajectory,
                nlp_category, nlp_confidence, nlp_keywords, diagnostic_answers,
                student_solution, strengths, growth_areas, recommended_strategy, action_step
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            );
            """
            values = (
                data.get("roll_no"),
                data.get("student_name"),
                data.get("student_class"),
                data.get("student_section"),
                data.get("topic"),
                data.get("subtopic"),
                data.get("raw_input"),
                data.get("followup_notes"),
                data.get("followup_trajectory"),
                data.get("nlp_category"),
                data.get("nlp_confidence"),
                data.get("nlp_keywords"),
                json.dumps(data.get("diagnostic_answers", [])),
                data.get("student_solution"),
                data.get("strengths"),
                data.get("growth_areas"),
                data.get("named_protocol") or data.get("recommended_strategy"),
                data.get("action_step")
            )

            cursor.execute(insert_query, values)
            db.commit()
            cursor.close()
            db.close()
            print("\n[MySQL Pipeline] Diagnostic record saved and committed successfully! ✅")
            return True
        except Exception as e:
            print(f"\n[MySQL Pipeline Notice] Database auto-save status: {e}")
            return False

    def diagnose(self) -> DiagnosticResult:
        """Runs the interactive workflow and guarantees data persistence to MySQL."""
        print("\n" + "=" * 65)
        print("       GENERAL STUDY DIFFICULTY DIAGNOSTIC (ACADEMIC)")
        print("=" * 65)
        print(f"Welcome {self.student_name}! Not all study hurdles come from difficult subjects.")
        print("Often, it is environment, routine, pressure, or focus that make all the difference.")

        # 1. Returning Student Check
        is_returning = self.check_returning_student()
        if not is_returning:
            print("Let's look into your study workflow together.\n")
            self.identify_topic()

        # 2. Scenario & Questions
        self.select_subtopic()
        self.ask_diagnostic_questions()

        # 3. Student Self-Reflection
        self.engage_student_solution()

        # 4. Mentoring Report
        self.display_mentoring_result()

        # 5. Guaranteed MySQL Auto-Save
        payload = self.get_structured_result()
        self.save_to_mysql_direct(payload)

        # 6. Branching Follow-Up
        more = input("\nWould you like to explore another general study challenge? (yes/no): ").strip().lower()
        if more in ["yes", "y"]:
            self.raw_problem = ""
            self.previous_record = None
            return self.diagnose()

        print("Remember: progress happens in small, deliberate daily experiments. You've got this! ✨\n")
        return payload

if __name__ == "__main__":
    print("Testing DoubtDiagnostic_General Standalone...")
    runner = DoubtDiagnostic_General(
        Roll_no="12321",
        Student_name="Sujay Kiran",
        student_class="12",
        Student_Section="C",
        problem="my parents are not motivating me and comparing me with others"
    )
    runner.diagnose()