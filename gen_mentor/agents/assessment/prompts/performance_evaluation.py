"""Prompts for performance evaluation."""

PERFORMANCE_EVALUATION_PROMPT = """
Evaluate the learner's performance based on the following information:

Learner Profile:
{learner_profile}

Learning Path:
{learning_path}

Session Data:
{session_data}

Quiz Results:
{quiz_results}

Provide a comprehensive performance evaluation including:

1. **Overall Performance Score** (0-100)
   - Calculate based on quiz results, engagement, and progress

2. **Strengths**
   - What the learner is doing well
   - Skills showing good progress

3. **Weaknesses**
   - Areas needing improvement
   - Concepts not fully understood

4. **Progress Assessment**
   - How well they're advancing through the learning path
   - Comparison to expected progress

5. **Skill-Specific Evaluations**
   - For each skill in the learning path, assess current proficiency
   - Identify skills ready to advance vs skills needing more practice

6. **Recommendations**
   - Specific actions to improve performance
   - Suggested focus areas for next session
   - Adaptive learning adjustments

Return your evaluation as JSON with the following structure:
{{
  "overall_score": <number 0-100>,
  "performance_level": "<excellent|good|satisfactory|needs_improvement>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
  "progress_status": {{
    "current_session": <number>,
    "expected_session": <number>,
    "on_track": <boolean>,
    "pace": "<ahead|on_pace|behind>"
  }},
  "skill_evaluations": [
    {{
      "skill_name": "<skill>",
      "current_level": "<unlearned|beginner|intermediate|advanced>",
      "confidence": "<low|medium|high>",
      "ready_to_advance": <boolean>,
      "notes": "<assessment notes>"
    }}
  ],
  "recommendations": [
    {{
      "priority": "<high|medium|low>",
      "action": "<recommended action>",
      "rationale": "<why this is recommended>"
    }}
  ],
  "next_steps": "<summary of next steps>"
}}
"""

SKILL_MASTERY_EVALUATION_PROMPT = """
Evaluate the learner's mastery of a specific skill:

Skill Name: {skill_name}

Learner Responses:
{learner_responses}

Quiz Results:
{quiz_results}

Previous Attempts:
{previous_attempts}

Assess the learner's mastery level for this skill:

1. **Understanding Level**
   - Conceptual understanding
   - Ability to apply the skill
   - Depth of knowledge

2. **Proficiency Assessment**
   - Current proficiency level (unlearned/beginner/intermediate/advanced)
   - Confidence in the assessment (low/medium/high)
   - Evidence supporting the assessment

3. **Progression Indicators**
   - Improvement from previous attempts
   - Ready to advance to next level?
   - Specific areas mastered

4. **Gap Analysis**
   - What's missing for full mastery
   - Common mistakes or misconceptions
   - Practice recommendations

Return your evaluation as JSON:
{{
  "skill_name": "{skill_name}",
  "current_level": "<unlearned|beginner|intermediate|advanced>",
  "confidence": "<low|medium|high>",
  "understanding_score": <number 0-100>,
  "proficiency_score": <number 0-100>,
  "ready_to_advance": <boolean>,
  "mastered_aspects": ["<aspect 1>", "<aspect 2>", ...],
  "gaps": ["<gap 1>", "<gap 2>", ...],
  "improvement_from_previous": "<improved|same|declined|no_previous_data>",
  "evidence": "<key evidence supporting this assessment>",
  "practice_recommendations": [
    "<specific practice recommendation 1>",
    "<specific practice recommendation 2>"
  ],
  "estimated_time_to_mastery": "<time estimate or 'already mastered'>"
}}
"""

PERFORMANCE_REPORT_PROMPT = """
Generate a comprehensive performance report for the learner:

Learner Profile:
{learner_profile}

Performance History:
{performance_history}

Time Period: {time_period}

Create a professional, encouraging, and actionable performance report that includes:

1. **Executive Summary**
   - Overall performance during the time period
   - Key achievements
   - Main challenges

2. **Progress Overview**
   - Learning goals and how much has been achieved
   - Skills mastered
   - Skills in progress
   - Overall trajectory (improving/stable/declining)

3. **Detailed Skill Assessment**
   - For each skill, provide:
     - Current proficiency level
     - Progress made during this period
     - Strengths in this skill area
     - Areas for improvement

4. **Engagement Metrics**
   - Session attendance/completion
   - Quiz performance trends
   - Interaction quality
   - Time investment

5. **Strengths and Achievements**
   - What the learner excels at
   - Notable improvements
   - Milestones reached

6. **Areas for Improvement**
   - Skills needing more attention
   - Common challenges
   - Suggested focus areas

7. **Recommendations**
   - Specific, actionable next steps
   - Study strategies
   - Resource suggestions
   - Timeline adjustments if needed

8. **Motivational Message**
   - Encouraging closing remarks
   - Recognition of effort
   - Positive outlook for continued learning

Format the report in clear, professional markdown with:
- Sections with headers
- Bullet points for lists
- Tables for comparative data if appropriate
- Emphasis on key points

Keep the tone supportive, encouraging, and focused on growth.
"""

__all__ = [
    "PERFORMANCE_EVALUATION_PROMPT",
    "SKILL_MASTERY_EVALUATION_PROMPT",
    "PERFORMANCE_REPORT_PROMPT",
]
