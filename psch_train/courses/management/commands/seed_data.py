from django.core.management.base import BaseCommand
from courses.models import Course, Quiz, Question, Choice, CourseContent
from patients.models import PatientScenario


class Command(BaseCommand):
    help = 'Seeds database with psychology courses, AI patients, and quiz questions'

    def handle(self, *args, **options):
        self.stdout.write('🔴 Seeding courses, patients, and quizzes...\n')

        # ═══════════════════════════════════════════════════════════
        # COURSE 1: Depression & Mood Disorders
        # ═══════════════════════════════════════════════════════════
        course1, _ = Course.objects.get_or_create(
            title="Depression & Mood Disorders",
            defaults={
                "description": "Learn to assess, diagnose, and provide therapeutic interventions for patients experiencing major depressive disorder, persistent depressive disorder, and bipolar spectrum disorders. Covers cognitive-behavioral techniques, motivational interviewing, and crisis assessment.",
                "difficulty": "beginner",
                "duration_hours": 4,
                "objectives": "• Identify core symptoms of Major Depressive Disorder\n• Conduct a depression severity assessment\n• Apply cognitive-behavioral techniques\n• Recognize warning signs and assess suicide risk",
                "order": 1
            }
        )

        # Course 1 Content
        CourseContent.objects.get_or_create(
            course=course1,
            title="Understanding Depression",
            defaults={
                "order": 1,
                "content": """## What is Depression?

Major Depressive Disorder (MDD) is more than feeling sad. It's a persistent condition that affects how a person thinks, feels, and handles daily activities.

### Core Symptoms (DSM-5)
At least 5 of the following symptoms must be present for 2+ weeks:

1. **Depressed mood** most of the day, nearly every day
2. **Anhedonia** - markedly diminished interest or pleasure in activities
3. **Weight changes** - significant loss or gain (>5% in a month)
4. **Sleep disturbance** - insomnia or hypersomnia
5. **Psychomotor changes** - agitation or retardation
6. **Fatigue** or loss of energy
7. **Worthlessness** or excessive guilt
8. **Concentration difficulties** or indecisiveness
9. **Suicidal ideation** - recurrent thoughts of death

### Key Point
At least one symptom must be either (1) depressed mood or (2) loss of interest/pleasure."""
            }
        )

        CourseContent.objects.get_or_create(
            course=course1,
            title="Assessment Techniques",
            defaults={
                "order": 2,
                "content": """## Assessing Depression Severity

### Validated Instruments
- **PHQ-9** (Patient Health Questionnaire-9)
- **BDI-II** (Beck Depression Inventory)
- **HAM-D** (Hamilton Depression Rating Scale)

### Clinical Interview Questions
Ask about:
- Duration and onset of symptoms
- Impact on functioning (work, relationships, self-care)
- Previous episodes and treatments
- Family history of mood disorders
- Substance use
- **Always assess suicide risk**

### Suicide Risk Assessment
1. Ask directly: "Are you having thoughts of hurting yourself?"
2. Assess: Ideation, Plan, Intent, Means, Timeline
3. Protective factors: Reasons for living, social support
4. Document thoroughly"""
            }
        )

        # Course 1 Patients
        PatientScenario.objects.get_or_create(
            course=course1,
            name="Marcus Johnson",
            defaults={
                "condition": "Major Depressive Disorder",
                "severity": "moderate",
                "persona_prompt": """You are Marcus Johnson, a 34-year-old accountant experiencing moderate major depressive disorder.

BACKGROUND:
- Recently divorced (6 months ago) after 8 years of marriage
- Two children (ages 5 and 7) who live with your ex-wife
- Work performance has declined; received a warning from supervisor
- Living alone in a small apartment

SYMPTOMS TO DISPLAY:
- Persistent sad mood, feeling "empty"
- Loss of interest in hobbies you once loved (golf, reading)
- Difficulty sleeping - wake up at 3-4 AM and can't fall back asleep
- Low energy, everything feels like enormous effort
- Difficulty concentrating at work
- Feelings of worthlessness and guilt about the divorce
- Decreased appetite, lost 15 pounds in 3 months

BEHAVIORAL GUIDELINES:
- Speak slowly, with pauses and sighs
- Avoid eye contact (mention looking down or away)
- Give short answers initially; open up gradually if therapist shows empathy
- Express ambivalence about getting help ("I don't know if talking will help")
- NO active suicidal ideation, but mention feeling like "what's the point"
- Show some hope when discussing your children"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course1,
            name="Sarah Chen",
            defaults={
                "condition": "Persistent Depressive Disorder (Dysthymia)",
                "severity": "mild",
                "persona_prompt": """You are Sarah Chen, a 28-year-old graduate student experiencing persistent depressive disorder (dysthymia).

BACKGROUND:
- PhD student in Biology, 4th year
- Has felt "low-grade depressed" for as long as you can remember
- High-achieving but never feels good enough
- Immigrant family; parents have high expectations
- Few close friends; tends to isolate

SYMPTOMS TO DISPLAY:
- Chronic low mood lasting years (not severe, but persistent)
- Low self-esteem, constant self-criticism
- Difficulty making decisions
- Feelings of hopelessness about the future
- Low energy but still functional
- Occasional overeating for comfort
- Sleep too much on weekends (10-12 hours)

BEHAVIORAL GUIDELINES:
- Articulate and intelligent but self-deprecating
- Minimize your problems ("Other people have it worse")
- Difficulty accepting compliments or positive feedback
- Express doubt that therapy can help after "feeling this way forever"
- Show curiosity about therapeutic techniques
- Mention pressure from family to succeed"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course1,
            name="David Williams",
            defaults={
                "condition": "Major Depressive Disorder with Suicidal Ideation",
                "severity": "severe",
                "persona_prompt": """You are David Williams, a 52-year-old former construction worker experiencing severe depression with passive suicidal ideation.

BACKGROUND:
- Lost job 8 months ago due to back injury
- Chronic pain from injury; takes pain medication
- Wife works extra hours to support family; feeling like a burden
- Adult son doesn't talk to him after an argument
- History of alcohol abuse (currently sober 2 years)

SYMPTOMS TO DISPLAY:
- Severe depressed mood, feels "hopeless"
- Passive suicidal ideation: "Sometimes I think my family would be better off without me"
- NO active plan or intent (important safety note)
- Significant psychomotor retardation - moves and speaks slowly
- Anhedonia - nothing brings pleasure anymore
- Sleep disturbance - sleeps 3-4 hours per night
- Feelings of being a burden to family
- Irritability and occasional anger

BEHAVIORAL GUIDELINES:
- Initially reluctant and skeptical of therapy ("Talking won't fix my back")
- May become emotional when discussing family
- Test the therapist's reaction when mentioning dark thoughts
- Respond positively to validation of pain and struggle
- Pride is important - don't want to seem weak
- If therapist handles suicidal ideation well, show relief at being heard

SAFETY NOTE: Display passive ideation only. If asked directly, confirm NO plan, NO intent, NO means selected."""
            }
        )

        # Course 1 Quiz
        quiz1, _ = Quiz.objects.get_or_create(
            course=course1,
            defaults={
                "title": "Depression & Mood Disorders Assessment",
                "description": "Test your knowledge of depression symptoms, diagnosis, and treatment approaches.",
                "passing_score": 70,
                "time_limit_minutes": 15
            }
        )

        self._create_question(quiz1, 1,
            "Which of the following is NOT a core symptom required for a Major Depressive Disorder diagnosis according to DSM-5?",
            "The two core symptoms are depressed mood and loss of interest/pleasure (anhedonia). At least one must be present. Irritability can occur but is not a core criterion for adults.",
            [
                ("Depressed mood most of the day", False),
                ("Markedly diminished interest or pleasure", False),
                ("Irritability and anger outbursts", True),
                ("Significant weight loss or gain", False),
            ]
        )

        self._create_question(quiz1, 2,
            "What is the minimum duration of symptoms required for a diagnosis of Major Depressive Disorder?",
            "MDD requires symptoms to be present for at least 2 weeks, representing a change from previous functioning.",
            [
                ("1 week", False),
                ("2 weeks", True),
                ("1 month", False),
                ("3 months", False),
            ]
        )

        self._create_question(quiz1, 3,
            "When assessing suicide risk, which approach is recommended?",
            "Research shows that asking directly about suicidal thoughts does not increase risk and allows for proper assessment and intervention.",
            [
                ("Avoid asking directly to prevent giving ideas", False),
                ("Only ask if the patient brings it up first", False),
                ("Ask directly and specifically about thoughts, plans, and intent", True),
                ("Use only standardized questionnaires without discussion", False),
            ]
        )

        self._create_question(quiz1, 4,
            "Persistent Depressive Disorder (Dysthymia) differs from Major Depressive Disorder primarily in:",
            "Dysthymia is characterized by chronic, less severe symptoms lasting at least 2 years, while MDD involves more severe episodes of at least 2 weeks.",
            [
                ("The types of symptoms experienced", False),
                ("Duration and severity of symptoms", True),
                ("Age of onset only", False),
                ("Response to medication", False),
            ]
        )

        self._create_question(quiz1, 5,
            "Which validated instrument is a 9-item self-report measure commonly used to screen for depression?",
            "The PHQ-9 (Patient Health Questionnaire-9) is a widely used, brief screening tool that assesses depression severity.",
            [
                ("BDI-II", False),
                ("HAM-D", False),
                ("PHQ-9", True),
                ("MADRS", False),
            ]
        )

        # ═══════════════════════════════════════════════════════════
        # COURSE 2: Anxiety Disorders
        # ═══════════════════════════════════════════════════════════
        course2, _ = Course.objects.get_or_create(
            title="Anxiety Disorders & Phobias",
            defaults={
                "description": "Comprehensive training on generalized anxiety disorder, panic disorder, social anxiety, and specific phobias. Learn exposure therapy principles, relaxation techniques, cognitive restructuring, and anxiety management strategies.",
                "difficulty": "beginner",
                "duration_hours": 4,
                "objectives": "• Differentiate between anxiety disorders\n• Understand the cognitive model of anxiety\n• Apply exposure therapy principles\n• Teach relaxation and grounding techniques",
                "order": 2
            }
        )

        CourseContent.objects.get_or_create(
            course=course2,
            title="Understanding Anxiety",
            defaults={
                "order": 1,
                "content": """## The Nature of Anxiety

Anxiety is a normal human emotion that becomes problematic when it's excessive, persistent, and interferes with daily functioning.

### Fight-Flight-Freeze Response
- Evolutionary survival mechanism
- Becomes maladaptive when triggered inappropriately
- Physical symptoms: racing heart, sweating, trembling, shortness of breath

### Types of Anxiety Disorders
1. **Generalized Anxiety Disorder (GAD)** - Excessive worry about multiple areas
2. **Panic Disorder** - Recurrent unexpected panic attacks
3. **Social Anxiety Disorder** - Fear of social/performance situations
4. **Specific Phobias** - Fear of specific objects/situations
5. **Agoraphobia** - Fear of situations where escape might be difficult

### The Anxiety Cycle
Trigger → Anxious thoughts → Physical symptoms → Avoidance → Short-term relief → Long-term maintenance"""
            }
        )

        # Course 2 Patients
        PatientScenario.objects.get_or_create(
            course=course2,
            name="Emily Roberts",
            defaults={
                "condition": "Generalized Anxiety Disorder",
                "severity": "moderate",
                "persona_prompt": """You are Emily Roberts, a 31-year-old marketing manager with generalized anxiety disorder.

BACKGROUND:
- Works at a demanding tech startup
- Recently promoted to manager; overwhelmed by new responsibilities
- Engaged to be married in 6 months
- Mother has history of anxiety
- Perfectionist tendencies since childhood

SYMPTOMS TO DISPLAY:
- Excessive worry about multiple areas (work, relationship, health, finances)
- Difficulty controlling worry - mind races with "what ifs"
- Muscle tension, especially in neck and shoulders
- Restlessness, feeling "keyed up"
- Difficulty falling asleep due to racing thoughts
- Irritability when stressed
- Difficulty concentrating - mind goes blank in meetings
- Seeking reassurance frequently

BEHAVIORAL GUIDELINES:
- Speak quickly, jump from topic to topic
- Ask therapist "Do you think everything will be okay?" seeking reassurance
- Intellectualize and analyze your anxiety
- Recognize anxiety is irrational but can't stop
- Mention physical symptoms (stomach issues, headaches)
- Show motivation for treatment - this is affecting your relationship"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course2,
            name="James Martinez",
            defaults={
                "condition": "Panic Disorder with Agoraphobia",
                "severity": "severe",
                "persona_prompt": """You are James Martinez, a 26-year-old software developer with panic disorder and developing agoraphobia.

BACKGROUND:
- Works remotely (which has enabled avoidance)
- First panic attack was 18 months ago in a crowded mall
- Now avoids driving, crowded places, being far from home
- Single, dating has become impossible
- Close relationship with sister who drives him to appointments

SYMPTOMS TO DISPLAY:
- Describe panic attacks vividly: racing heart, can't breathe, dizziness, feeling of dying
- Fear of having another panic attack
- Avoidance of triggers: crowds, driving, elevators, being alone
- Hypervigilance to body sensations
- Constantly checking heart rate and breathing
- Fear of "going crazy" or losing control
- Anticipatory anxiety before leaving house

BEHAVIORAL GUIDELINES:
- Show visible anxiety when discussing panic attacks
- Ask if panic attacks can cause heart attacks (health anxiety component)
- Express frustration at how limited your life has become
- Show insight that avoidance makes it worse but feel unable to stop
- Mention embarrassment about this affecting a "grown man"
- Be receptive to psychoeducation about panic"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course2,
            name="Aisha Patel",
            defaults={
                "condition": "Social Anxiety Disorder",
                "severity": "moderate",
                "persona_prompt": """You are Aisha Patel, a 22-year-old recent college graduate with social anxiety disorder.

BACKGROUND:
- Graduated with honors in Computer Science
- Struggling to attend job interviews due to anxiety
- Living with parents who are supportive but worried
- Had a small friend group in college, now feels isolated
- Avoids phone calls, prefers texting

SYMPTOMS TO DISPLAY:
- Intense fear of being judged or embarrassed
- Avoid speaking in groups, even small ones
- Physical symptoms in social situations: blushing, trembling, sweating
- Replay social interactions afterward, cringing at perceived mistakes
- Difficulty with authority figures
- Avoidance of eating in public
- Speak quietly, with hesitation

BEHAVIORAL GUIDELINES:
- Take time to answer questions; long pauses are okay
- Look down or away when discussing embarrassing moments
- Apologize frequently ("Sorry, I'm not explaining this well")
- Show self-awareness about the irrationality of fears
- Express sadness about missed opportunities
- Mention that therapy itself is anxiety-provoking
- Gradually open up as trust builds"""
            }
        )

        # Course 2 Quiz
        quiz2, _ = Quiz.objects.get_or_create(
            course=course2,
            defaults={
                "title": "Anxiety Disorders Assessment",
                "description": "Test your understanding of anxiety disorders, their presentation, and treatment approaches.",
                "passing_score": 70,
                "time_limit_minutes": 15
            }
        )

        self._create_question(quiz2, 1,
            "What is the primary mechanism that maintains anxiety disorders over time?",
            "Avoidance provides short-term relief but prevents learning that feared situations are manageable, maintaining the anxiety cycle long-term.",
            [
                ("Genetic predisposition", False),
                ("Avoidance behaviors", True),
                ("Medication side effects", False),
                ("Lack of social support", False),
            ]
        )

        self._create_question(quiz2, 2,
            "During a panic attack, a patient believes they are having a heart attack. This is an example of:",
            "Catastrophic misinterpretation of bodily sensations is a hallmark of panic disorder, where normal anxiety symptoms are interpreted as dangerous.",
            [
                ("Delusional thinking", False),
                ("Catastrophic misinterpretation", True),
                ("Somatic symptom disorder", False),
                ("Illness anxiety disorder", False),
            ]
        )

        self._create_question(quiz2, 3,
            "Which therapeutic approach has the strongest evidence base for treating anxiety disorders?",
            "Cognitive-Behavioral Therapy (CBT), particularly with exposure components, has the strongest empirical support for anxiety disorders.",
            [
                ("Psychoanalysis", False),
                ("Cognitive-Behavioral Therapy (CBT)", True),
                ("Humanistic therapy", False),
                ("Supportive counseling alone", False),
            ]
        )

        self._create_question(quiz2, 4,
            "In exposure therapy, what is the goal of having a patient face their feared stimulus?",
            "Exposure allows habituation (anxiety naturally decreases) and new learning (the feared outcome doesn't occur or is manageable).",
            [
                ("To increase their anxiety tolerance permanently", False),
                ("To allow habituation and corrective learning", True),
                ("To prove the therapist is in control", False),
                ("To exhaust the patient's nervous system", False),
            ]
        )

        self._create_question(quiz2, 5,
            "A patient with social anxiety avoids all job interviews. The therapist should first:",
            "Building a hierarchy allows systematic exposure starting with less threatening situations, increasing chances of success.",
            [
                ("Encourage them to immediately attend a group interview", False),
                ("Suggest they only apply for remote jobs", False),
                ("Build an exposure hierarchy from least to most anxiety-provoking", True),
                ("Focus only on relaxation techniques", False),
            ]
        )

        # ═══════════════════════════════════════════════════════════
        # COURSE 3: Trauma & PTSD
        # ═══════════════════════════════════════════════════════════
        course3, _ = Course.objects.get_or_create(
            title="Trauma-Informed Care & PTSD",
            defaults={
                "description": "Learn trauma-informed approaches, PTSD assessment, and evidence-based treatments including prolonged exposure and cognitive processing therapy. Emphasis on creating safety, building trust, and avoiding retraumatization.",
                "difficulty": "intermediate",
                "duration_hours": 6,
                "objectives": "• Understand trauma responses and PTSD criteria\n• Apply trauma-informed principles\n• Recognize signs of dissociation\n• Maintain appropriate boundaries while showing compassion",
                "order": 3
            }
        )

        CourseContent.objects.get_or_create(
            course=course3,
            title="Trauma-Informed Principles",
            defaults={
                "order": 1,
                "content": """## What is Trauma?

Trauma results from an event or series of events experienced as physically or emotionally harmful, with lasting adverse effects on functioning.

### The 6 Principles of Trauma-Informed Care
1. **Safety** - Physical and emotional safety for patient and staff
2. **Trustworthiness & Transparency** - Building trust through clear, consistent communication
3. **Peer Support** - Connecting with others who have shared experiences
4. **Collaboration & Mutuality** - Sharing power, leveling power differences
5. **Empowerment & Choice** - Prioritizing patient choice and control
6. **Cultural, Historical & Gender Issues** - Recognizing and addressing biases

### PTSD Symptom Clusters (DSM-5)
1. **Intrusion** - Flashbacks, nightmares, intrusive memories
2. **Avoidance** - Avoiding reminders of trauma
3. **Negative Cognitions/Mood** - Blame, shame, emotional numbing
4. **Arousal/Reactivity** - Hypervigilance, startle response, sleep problems"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course3,
            name="Michael Torres",
            defaults={
                "condition": "PTSD (Combat-Related)",
                "severity": "severe",
                "persona_prompt": """You are Michael Torres, a 38-year-old military veteran with combat-related PTSD.

BACKGROUND:
- Served two tours in Afghanistan (2010-2014)
- Witnessed IED explosion that killed two close friends
- Honorably discharged, now works in warehouse
- Married with one child (age 3)
- Wife encouraged him to seek help; marriage is strained

SYMPTOMS TO DISPLAY:
- Intrusive memories and nightmares about the explosion
- Flashbacks triggered by loud noises (will mention jumping at sounds)
- Hypervigilance - always scanning for threats, sits with back to wall
- Emotional numbing - difficulty feeling love for family
- Avoidance of news about war, veterans' events
- Sleep difficulties, often stays up late "on guard"
- Anger outbursts that scare him
- Guilt about surviving when friends didn't

BEHAVIORAL GUIDELINES:
- Stoic demeanor; trained to suppress emotions
- Test the therapist ("Have you ever been in combat?")
- Initially dismissive ("I've dealt with worse")
- Show vulnerability when discussing guilt and family
- Distrust of "outsiders" but willing to try for family
- DO NOT go into graphic details of trauma unprompted
- Respond to respect and directness"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course3,
            name="Rachel Kim",
            defaults={
                "condition": "PTSD (Sexual Assault)",
                "severity": "moderate",
                "persona_prompt": """You are Rachel Kim, a 25-year-old nurse with PTSD following sexual assault.

BACKGROUND:
- Assaulted 2 years ago at a party by an acquaintance
- Did not report to police (common response)
- Threw herself into work afterward; recently symptoms worsening
- Close friend knows; family does not
- Previously enjoyed social life, now avoids parties and dating

SYMPTOMS TO DISPLAY:
- Intrusive thoughts and nightmares
- Avoidance of places, people, or situations resembling the trauma
- Difficulty trusting men, especially in professional settings
- Self-blame and shame ("I shouldn't have had that drink")
- Hyperarousal - easily startled, difficulty sleeping
- Feeling detached from others
- Moments of dissociation when stressed

BEHAVIORAL GUIDELINES:
- Be cautious initially; trust must be earned
- Appreciate being given control ("Is it okay if I ask about...")
- May become tearful when discussing the assault
- Express anger at societal responses to assault survivors
- Show strength and resilience alongside vulnerability
- DO NOT disclose graphic details; boundaries are important
- Test the therapist for any victim-blaming responses"""
            }
        )

        # Course 3 Quiz
        quiz3, _ = Quiz.objects.get_or_create(
            course=course3,
            defaults={
                "title": "Trauma-Informed Care Assessment",
                "description": "Test your knowledge of trauma-informed principles and PTSD treatment.",
                "passing_score": 70,
                "time_limit_minutes": 15
            }
        )

        self._create_question(quiz3, 1,
            "Which is NOT one of the six principles of trauma-informed care?",
            "The six principles are: Safety, Trustworthiness, Peer Support, Collaboration, Empowerment, and Cultural/Historical Awareness. Confrontation is not a principle.",
            [
                ("Safety", False),
                ("Trustworthiness and Transparency", False),
                ("Confrontation of avoidance", True),
                ("Empowerment and Choice", False),
            ]
        )

        self._create_question(quiz3, 2,
            "A trauma survivor suddenly appears 'spaced out' and unresponsive during session. This may indicate:",
            "Dissociation is a protective response to overwhelming stress, often seen in trauma survivors when triggered.",
            [
                ("Boredom with therapy", False),
                ("Dissociation", True),
                ("Medication side effects", False),
                ("Deliberate avoidance", False),
            ]
        )

        self._create_question(quiz3, 3,
            "When working with trauma survivors, why is giving the patient choices important?",
            "Trauma often involves loss of control. Providing choices helps restore sense of agency and avoids retraumatization.",
            [
                ("It makes sessions go faster", False),
                ("It helps restore sense of control lost during trauma", True),
                ("It reduces therapist liability", False),
                ("It is required by licensing boards", False),
            ]
        )

        self._create_question(quiz3, 4,
            "Survivor's guilt is best described as:",
            "Survivor's guilt involves feelings of guilt about surviving when others did not, or believing one should have done more to prevent others' harm.",
            [
                ("Guilt about not preventing the trauma", False),
                ("Guilt about surviving when others did not", True),
                ("Guilt about seeking therapy", False),
                ("Guilt about symptoms interfering with work", False),
            ]
        )

        self._create_question(quiz3, 5,
            "Which approach should be AVOIDED when a patient discloses trauma?",
            "Pushing for details before the patient is ready can be retraumatizing. Patient should control the pace of disclosure.",
            [
                ("Validating their experience", False),
                ("Expressing belief in their account", False),
                ("Immediately asking for detailed description of the event", True),
                ("Offering a tissue if they become emotional", False),
            ]
        )

        # ═══════════════════════════════════════════════════════════
        # COURSE 4: Personality Disorders
        # ═══════════════════════════════════════════════════════════
        course4, _ = Course.objects.get_or_create(
            title="Working with Personality Disorders",
            defaults={
                "description": "Specialized training on Cluster B personality disorders including borderline and narcissistic presentations. Learn dialectical behavior therapy skills, managing countertransference, setting therapeutic boundaries, and building alliance with challenging patients.",
                "difficulty": "advanced",
                "duration_hours": 8,
                "objectives": "• Understand personality disorder patterns\n• Apply DBT principles\n• Set and maintain therapeutic boundaries\n• Manage countertransference reactions",
                "order": 4
            }
        )

        CourseContent.objects.get_or_create(
            course=course4,
            title="Understanding Personality Disorders",
            defaults={
                "order": 1,
                "content": """## What are Personality Disorders?

Personality disorders are enduring patterns of inner experience and behavior that deviate from cultural expectations, are pervasive and inflexible, and cause distress or impairment.

### Cluster B Personality Disorders
- **Borderline PD**: Instability in relationships, self-image, emotions; fear of abandonment
- **Narcissistic PD**: Grandiosity, need for admiration, lack of empathy
- **Antisocial PD**: Disregard for others' rights, manipulation, lack of remorse
- **Histrionic PD**: Excessive emotionality and attention-seeking

### Key Therapeutic Principles
1. **Consistency** - Maintain stable boundaries and expectations
2. **Validation** - Acknowledge emotions while not reinforcing maladaptive behaviors
3. **Balance** - Acceptance AND change (DBT dialectic)
4. **Self-awareness** - Monitor your own reactions (countertransference)"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course4,
            name="Olivia Bennett",
            defaults={
                "condition": "Borderline Personality Disorder",
                "severity": "moderate",
                "persona_prompt": """You are Olivia Bennett, a 29-year-old barista with borderline personality disorder.

BACKGROUND:
- History of unstable relationships
- Father abandoned family at age 7; mother emotionally unavailable
- Self-harm history (cutting) - currently 6 months clean
- Multiple previous therapists ("None of them understood me")
- Recently broke up with boyfriend; devastated

SYMPTOMS TO DISPLAY:
- Fear of abandonment - very sensitive to perceived rejection
- Unstable relationships - idealization followed by devaluation
- Identity disturbance - unclear sense of self
- Emotional instability - rapid mood shifts
- Chronic feelings of emptiness
- Impulsive behaviors (spending, risky sex when distressed)
- Black-and-white thinking

BEHAVIORAL GUIDELINES:
- Initially idealize the therapist ("You actually get me unlike the others")
- Test boundaries (ask personal questions, request extra sessions)
- Shift quickly between emotions during session
- If feeling misunderstood, become angry or withdrawn
- Express fear that therapist will abandon you too
- Show insight during calm moments
- Respond well to validation of emotions
- May mention passive suicidal thoughts when distressed (no active plan)"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course4,
            name="Alexander Price",
            defaults={
                "condition": "Narcissistic Personality Traits",
                "severity": "mild",
                "persona_prompt": """You are Alexander Price, a 45-year-old sales executive with narcissistic personality traits.

BACKGROUND:
- Highly successful in career; CEO of mid-size company
- Wife recently filed for divorce citing emotional neglect
- Attending therapy at wife's ultimatum
- Raised by demanding parents who praised achievement only
- Never previously in therapy; views it as weakness

SYMPTOMS TO DISPLAY:
- Grandiosity - emphasize your success and importance
- Need for admiration - drop hints about achievements
- Lack of empathy - difficulty understanding wife's complaints
- Entitlement - expect special treatment
- Arrogant behaviors - may condescend to therapist
- Underneath: fragile self-esteem, fear of failure

BEHAVIORAL GUIDELINES:
- Question therapist's credentials initially
- Struggle to see your role in marital problems
- Intellectualize emotions; avoid vulnerability
- Become defensive when receiving feedback
- Show glimpses of pain when discussing childhood
- Gradually acknowledge that something must change
- Respond to therapist who doesn't challenge but gently reflects"""
            }
        )

        # Course 4 Quiz
        quiz4, _ = Quiz.objects.get_or_create(
            course=course4,
            defaults={
                "title": "Personality Disorders Assessment",
                "description": "Test your knowledge of personality disorders and therapeutic approaches.",
                "passing_score": 70,
                "time_limit_minutes": 15
            }
        )

        self._create_question(quiz4, 1,
            "A patient with BPD initially praises you as 'the best therapist ever' then angrily criticizes you weeks later. This pattern is called:",
            "Splitting (idealization and devaluation) is a defense mechanism common in BPD where people are seen as all good or all bad.",
            [
                ("Transference", False),
                ("Splitting", True),
                ("Projection", False),
                ("Dissociation", False),
            ]
        )

        self._create_question(quiz4, 2,
            "The core dialectic in DBT (Dialectical Behavior Therapy) is between:",
            "DBT balances validation/acceptance with pushing for change - both are necessary for progress.",
            [
                ("Past and present", False),
                ("Acceptance and change", True),
                ("Individual and group therapy", False),
                ("Medication and therapy", False),
            ]
        )

        self._create_question(quiz4, 3,
            "When a patient with narcissistic traits becomes defensive, the therapist should:",
            "Gentle, non-confrontational reflection maintains alliance while still addressing issues. Direct confrontation often backfires.",
            [
                ("Directly confront their defensiveness", False),
                ("Provide evidence against their grandiosity", False),
                ("Use gentle, non-confrontational reflection", True),
                ("End the session immediately", False),
            ]
        )

        self._create_question(quiz4, 4,
            "A BPD patient asks for your personal phone number 'for emergencies.' The best response is:",
            "Clear boundaries with alternatives maintain safety while acknowledging the patient's distress.",
            [
                ("Give it to them to build trust", False),
                ("Refuse and explore what's driving the request", True),
                ("Report them to your supervisor", False),
                ("Agree but never answer when they call", False),
            ]
        )

        self._create_question(quiz4, 5,
            "Countertransference reactions are MOST important to monitor when working with personality disorders because:",
            "Strong reactions can impact treatment; awareness allows for appropriate management rather than acting out.",
            [
                ("Licensing boards require documentation", False),
                ("These patients often evoke strong reactions that can affect treatment", True),
                ("Insurance requires it for reimbursement", False),
                ("It makes supervision easier", False),
            ]
        )

        # ═══════════════════════════════════════════════════════════
        # COURSE 5: Substance Use Disorders
        # ═══════════════════════════════════════════════════════════
        course5, _ = Course.objects.get_or_create(
            title="Substance Use & Addiction Counseling",
            defaults={
                "description": "Training on assessment and treatment of alcohol and substance use disorders. Learn motivational interviewing, stages of change model, relapse prevention, and how to work with ambivalence about recovery.",
                "difficulty": "intermediate",
                "duration_hours": 5,
                "objectives": "• Apply Motivational Interviewing techniques\n• Understand stages of change\n• Conduct substance use assessments\n• Develop relapse prevention plans",
                "order": 5
            }
        )

        CourseContent.objects.get_or_create(
            course=course5,
            title="Motivational Interviewing Basics",
            defaults={
                "order": 1,
                "content": """## Motivational Interviewing (MI)

MI is a collaborative, goal-oriented style of communication designed to strengthen personal motivation for change.

### The Spirit of MI
- **Partnership** - Collaborate rather than prescribe
- **Acceptance** - Respect autonomy, affirm strengths
- **Compassion** - Prioritize patient's welfare
- **Evocation** - Draw out patient's own motivations

### Core Skills (OARS)
- **Open questions** - Invite elaboration
- **Affirmations** - Recognize strengths and efforts
- **Reflections** - Demonstrate understanding, deepen exploration
- **Summaries** - Collect and link what's been said

### Stages of Change
1. **Precontemplation** - Not considering change
2. **Contemplation** - Ambivalent, weighing pros/cons
3. **Preparation** - Planning to change soon
4. **Action** - Actively making changes
5. **Maintenance** - Sustaining changes
6. **Relapse** - Return to old behaviors (part of process)"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course5,
            name="Brian Murphy",
            defaults={
                "condition": "Alcohol Use Disorder",
                "severity": "moderate",
                "persona_prompt": """You are Brian Murphy, a 41-year-old teacher with alcohol use disorder.

BACKGROUND:
- High school history teacher, well-liked by students
- Drinking escalated during pandemic; now 8-10 drinks nightly
- Wife threatened to leave; taking kids to her mother's
- Hiding drinking from coworkers; performance declining
- Father was an alcoholic; swore you'd never be like him

SYMPTOMS TO DISPLAY:
- Drinking more than intended
- Multiple failed attempts to cut back
- Spending significant time drinking or recovering
- Cravings for alcohol in evenings
- Neglecting responsibilities
- Withdrawal symptoms if not drinking (tremors, anxiety)
- Continued use despite relationship problems

BEHAVIORAL GUIDELINES:
- Ambivalent about being called an "alcoholic"
- Minimize drinking ("I only drink at home, not like a real alcoholic")
- Rationalize ("Teaching is stressful; I need to unwind")
- Show genuine fear of losing family
- Become defensive if feeling judged
- Respond well to reflective listening
- Express shame about becoming like father
- Show readiness for change varying throughout session"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course5,
            name="Crystal Washington",
            defaults={
                "condition": "Opioid Use Disorder",
                "severity": "severe",
                "persona_prompt": """You are Crystal Washington, a 33-year-old former nurse with opioid use disorder.

BACKGROUND:
- Started with pain pills after back surgery 5 years ago
- Lost nursing license when caught diverting medication
- Progressed to heroin when pills became expensive
- Currently on Suboxone (medication-assisted treatment)
- Living in sober house; estranged from family
- 60 days clean; longest streak in 3 years

SYMPTOMS TO DISPLAY:
- History of tolerance and withdrawal
- Previous overdose (2 years ago, revived with Narcan)
- Cravings, especially when stressed
- Anxiety about long-term recovery
- Grief about lost career and relationships
- Shame about "how far I fell"

BEHAVIORAL GUIDELINES:
- Know recovery terminology; experienced in treatment
- Be wary of judgment about past heroin use
- Express pride in current clean time
- Show vulnerability about fears of relapse
- Discuss the disease model of addiction with understanding
- Mention specific triggers (running into old using friends)
- Express cautious hope about rebuilding life
- Appreciate being treated as a person, not just an addict"""
            }
        )

        # Course 5 Quiz
        quiz5, _ = Quiz.objects.get_or_create(
            course=course5,
            defaults={
                "title": "Substance Use Disorders Assessment",
                "description": "Test your knowledge of addiction treatment and motivational interviewing.",
                "passing_score": 70,
                "time_limit_minutes": 15
            }
        )

        self._create_question(quiz5, 1,
            "In Motivational Interviewing, when a patient expresses reasons for change, this is called:",
            "Change talk is patient language that favors movement toward change. Evoking and reinforcing change talk is a key MI skill.",
            [
                ("Resistance", False),
                ("Change talk", True),
                ("Compliance", False),
                ("Insight", False),
            ]
        )

        self._create_question(quiz5, 2,
            "A patient says 'I know I drink too much, but it's the only way I can relax.' Which stage of change best describes this?",
            "Contemplation involves ambivalence - recognizing problems while also having reasons to continue the behavior.",
            [
                ("Precontemplation", False),
                ("Contemplation", True),
                ("Preparation", False),
                ("Action", False),
            ]
        )

        self._create_question(quiz5, 3,
            "What is the recommended response when a patient minimizes their substance use?",
            "MI uses reflective listening rather than confrontation, allowing the patient to hear and evaluate their own statements.",
            [
                ("Present evidence of the severity of their use", False),
                ("Use reflective listening to explore ambivalence", True),
                ("Refer immediately to inpatient treatment", False),
                ("Confront denial directly", False),
            ]
        )

        self._create_question(quiz5, 4,
            "Medication-Assisted Treatment (MAT) for opioid use disorder:",
            "MAT with medications like Suboxone or methadone is evidence-based and reduces mortality, overdose, and relapse.",
            [
                ("Is just substituting one addiction for another", False),
                ("Is evidence-based and improves outcomes", True),
                ("Should only be used short-term", False),
                ("Is ineffective without residential treatment", False),
            ]
        )

        self._create_question(quiz5, 5,
            "Relapse is best understood as:",
            "The stages of change model recognizes relapse as common and part of the process, not failure.",
            [
                ("Treatment failure requiring discharge", False),
                ("Evidence of poor motivation", False),
                ("A common part of the recovery process", True),
                ("A sign that outpatient treatment isn't working", False),
            ]
        )

        # ═══════════════════════════════════════════════════════════
        # COURSE 6: Child & Adolescent Psychology
        # ═══════════════════════════════════════════════════════════
        course6, _ = Course.objects.get_or_create(
            title="Child & Adolescent Therapy",
            defaults={
                "description": "Learn developmentally appropriate therapeutic approaches for children and teens. Covers ADHD, oppositional behaviors, school refusal, adolescent depression, and family systems interventions.",
                "difficulty": "intermediate",
                "duration_hours": 6,
                "objectives": "• Adapt therapeutic approach for developmental level\n• Engage reluctant adolescent clients\n• Work collaboratively with parents/caregivers\n• Recognize presentations unique to youth",
                "order": 6
            }
        )

        CourseContent.objects.get_or_create(
            course=course6,
            title="Working with Adolescents",
            defaults={
                "order": 1,
                "content": """## Engaging Adolescent Clients

Adolescents often don't choose to be in therapy, making engagement crucial.

### Unique Considerations
- **Developmental stage**: Identity formation, autonomy needs
- **Confidentiality concerns**: Balance teen privacy with safety
- **Power dynamics**: Avoid recreating parent-child dynamic
- **Communication style**: Be genuine, not "trying too hard"

### Strategies for Engagement
1. **Acknowledge their perspective** - Validate frustration about being "forced" to attend
2. **Explain confidentiality clearly** - What you will and won't share with parents
3. **Give them choices** - Seating, topics, activities
4. **Find their interests** - Connect through music, games, sports
5. **Be authentic** - Teens detect phoniness quickly

### Depression in Adolescents
Presents differently than in adults:
- May show as **irritability** rather than sadness
- Somatic complaints (headaches, stomachaches)
- Academic decline
- Social withdrawal OR acting out
- Sleep changes (often hypersomnia)"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course6,
            name="Tyler Anderson",
            defaults={
                "condition": "ADHD with Oppositional Behaviors",
                "severity": "moderate",
                "persona_prompt": """You are Tyler Anderson, a 14-year-old boy with ADHD and oppositional behaviors. You are being made to attend therapy by your parents.

BACKGROUND:
- Diagnosed with ADHD at age 8; on medication but doesn't like taking it
- Frequent conflicts with parents, especially about homework and chores
- Smart but underperforming in school
- Has friends but gets in trouble for being "class clown"
- Enjoys video games; parents restrict screen time leading to arguments
- Younger sister is "perfect" in your view (resentment)

SYMPTOMS TO DISPLAY:
- Restless - fidget, mention wanting to move around
- Impulsive responses
- Argues with adult decisions
- Defies rules at home
- Blames others for mistakes
- Easily annoyed
- Can also show: humor, creativity, and genuine caring underneath

BEHAVIORAL GUIDELINES:
- Initially resistant and monosyllabic ("I dunno," "Whatever")
- Question why you have to be here ("It's my parents' problem")
- Test the therapist's reaction to mild defiance
- Show interest if therapist is genuine and not "fake adult"
- Open up about feeling misunderstood and frustrated
- Respond well to being treated with respect, not lectured
- Show that you actually do care about family, just feel like the scapegoat"""
            }
        )

        PatientScenario.objects.get_or_create(
            course=course6,
            name="Maya Collins",
            defaults={
                "condition": "Adolescent Depression with School Refusal",
                "severity": "moderate",
                "persona_prompt": """You are Maya Collins, a 16-year-old girl experiencing depression and school refusal.

BACKGROUND:
- Sophomore in high school; hasn't attended in 3 weeks
- Was bullied last year; rumors spread about her online
- Parents divorced 2 years ago; lives with mom
- Used to be a good student and dancer
- Quit dance team; stopped talking to friends
- Spends most time in room on phone

SYMPTOMS TO DISPLAY:
- Low mood, tearful at times
- Loss of interest in dance and friends
- Sleep disturbance - stays up late, can't wake for school
- Low self-worth ("Everyone hates me anyway")
- Anxiety about returning to school
- Passive suicidal ideation ("I wish I could just disappear")
- Social media comparison making her feel worse

BEHAVIORAL GUIDELINES:
- Quiet but not entirely closed off
- Respond to genuine warmth and patience
- Reluctant to discuss bullying details
- Express feeling like a burden to mom
- Show anger at bullies and at herself
- Feel overwhelmed by thought of returning to school
- Appreciate validation that her feelings make sense
- Show small sparks of interest in things you used to love

SAFETY: Passive ideation only ("disappear"), NO active plan or intent. Will deny plan if asked directly."""
            }
        )

        # Course 6 Quiz
        quiz6, _ = Quiz.objects.get_or_create(
            course=course6,
            defaults={
                "title": "Child & Adolescent Therapy Assessment",
                "description": "Test your knowledge of working therapeutically with young people.",
                "passing_score": 70,
                "time_limit_minutes": 15
            }
        )

        self._create_question(quiz6, 1,
            "How does depression often present differently in adolescents compared to adults?",
            "Adolescent depression frequently manifests as irritability rather than the classic sad mood seen in adults.",
            [
                ("More severe suicidal ideation", False),
                ("Irritability more prominent than sadness", True),
                ("Complete lack of emotion", False),
                ("Identical presentation", False),
            ]
        )

        self._create_question(quiz6, 2,
            "When beginning therapy with a reluctant adolescent, the BEST first approach is to:",
            "Acknowledging their experience and giving choices establishes respect and begins building alliance.",
            [
                ("Immediately establish rules and expectations", False),
                ("Focus on what parents have reported", False),
                ("Acknowledge their feelings about being there and give them choices", True),
                ("Use play therapy techniques", False),
            ]
        )

        self._create_question(quiz6, 3,
            "Regarding confidentiality with adolescent clients, the therapist should:",
            "Clear, upfront communication about confidentiality limits builds trust with teens.",
            [
                ("Keep everything completely confidential from parents", False),
                ("Share everything with parents", False),
                ("Explain confidentiality and its limits clearly at the start", True),
                ("Avoid discussing confidentiality to prevent anxiety", False),
            ]
        )

        self._create_question(quiz6, 4,
            "A 13-year-old with ADHD is defiant in session. The therapist should understand this may reflect:",
            "Oppositional behavior often stems from frustration with perceived unfairness and feeling misunderstood.",
            [
                ("A conduct disorder diagnosis", False),
                ("Frustration with feeling misunderstood or unfairly treated", True),
                ("A need for stricter parenting", False),
                ("Medication non-compliance", False),
            ]
        )

        self._create_question(quiz6, 5,
            "School refusal in adolescents is best addressed by:",
            "Graduated return with support addresses avoidance while building confidence and skills.",
            [
                ("Forcing immediate full-time return to school", False),
                ("Allowing indefinite home schooling", False),
                ("Developing a gradual return plan with appropriate supports", True),
                ("Waiting until the teen is ready to return on their own", False),
            ]
        )

        self.stdout.write(self.style.SUCCESS('''
╔══════════════════════════════════════════════════════════════╗
║                  🔴 SEED DATA CREATED 🔴                     ║
╠══════════════════════════════════════════════════════════════╣
║  ✓ 6 Psychology Courses with Content                         ║
║  ✓ 12 AI Patient Scenarios                                   ║
║  ✓ 6 Course Quizzes (30 Questions Total)                     ║
╠══════════════════════════════════════════════════════════════╣
║  COURSES:                                                    ║
║    1. Depression & Mood Disorders (3 patients, 5 questions)  ║
║    2. Anxiety Disorders & Phobias (3 patients, 5 questions)  ║
║    3. Trauma-Informed Care & PTSD (2 patients, 5 questions)  ║
║    4. Working with Personality Disorders (2 patients, 5 q's) ║
║    5. Substance Use & Addiction (2 patients, 5 questions)    ║
║    6. Child & Adolescent Therapy (2 patients, 5 questions)   ║
╚══════════════════════════════════════════════════════════════╝
        '''))

    def _create_question(self, quiz, order, text, explanation, choices):
        """Helper to create questions with choices"""
        question, created = Question.objects.get_or_create(
            quiz=quiz,
            text=text,
            defaults={"order": order, "explanation": explanation}
        )
        if created:
            for choice_text, is_correct in choices:
                Choice.objects.get_or_create(
                    question=question,
                    text=choice_text,
                    defaults={"is_correct": is_correct}
                )
        return question
