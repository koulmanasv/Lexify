const questions = [
    {
        title: "Theft vs. Criminal Breach of Trust",
        question: "Ravi works as a cashier at a bank. During his shift, he takes ₹50,000 from the cash drawer and uses it to pay his son's medical bills, intending to replace it with his salary next month. However, he's caught before he can return the money. What should Ravi be charged with?",
        options: [
            "Section 378 IPC - Theft (Taking movable property without consent)",
            "Section 408 IPC - Criminal Breach of Trust by servant (Most appropriate)",
            "Section 405 IPC - Simple Criminal Breach of Trust",
            "Section 420 IPC - Cheating and dishonestly inducing delivery"
        ],
        correct: 1,
        explanation: "Section 408 is most appropriate as Ravi was entrusted with bank money in his capacity as cashier and dishonestly used it. Criminal breach of trust by servant applies when someone in employment misuses entrusted property.",
        hint: "Key Sections: 405 (Criminal Breach of Trust), 408 (by servant), 378 (Theft)",
        caselaw: "Jaswant Singh vs. State of Punjab - Employees entrusted with employer's property who misuse it are liable under Section 408."
    },
    {
        title: "Culpable Homicide vs. Murder",
        question: "During a heated argument at a wedding, Arjun pushes Vikram hard in anger. Vikram falls, hits his head on concrete steps, and dies instantly. Arjun never intended to kill Vikram. What is the appropriate charge?",
        options: [
            "Section 300 IPC - Murder (Intent to cause death)",
            "Section 299 IPC - Culpable homicide not amounting to murder (Most appropriate)",
            "Section 304 IPC - Culpable homicide not amounting to murder (punishment)",
            "Section 302 IPC - Punishment for murder"
        ],
        correct: 2,
        explanation: "Section 304 IPC (punishment provision for culpable homicide not amounting to murder) applies. Arjun had no intention to kill, only pushed in anger. The death was caused by knowledge that the act was likely to cause death but without intention to kill.",
        hint: "Key distinction: Intent to kill (murder) vs. knowledge likely to cause death (culpable homicide)",
        caselaw: "Reg vs. Govinda - Distinguished between intention and knowledge in homicide cases."
    },
    {
        title: "Right of Private Defense",
        question: "Late at night, Priya is walking home when three men surround her and demand her jewelry. When one man grabs her arm, she stabs him with a small knife, causing serious injuries. The man survives. Was Priya's response legally justified?",
        options: [
            "Yes, completely justified under Section 100 IPC (right to cause death in self-defense)",
            "No, excessive force - should be charged with voluntarily causing hurt",
            "Yes, justified under Section 96-99 IPC (proportionate self-defense) (Most appropriate)",
            "Partially justified - she should have tried to escape first"
        ],
        correct: 2,
        explanation: "Section 96-99 IPC provides right of private defense. Priya's response was proportionate to the threat. She was outnumbered, grabbed against her will, and used reasonable force to defend herself. No duty to retreat when faced with imminent danger.",
        hint: "Sections 96-106 deal with private defense of person and property",
        caselaw: "Darshan Singh vs. State - Self-defense must be proportionate but victim has no duty to retreat when faced with imminent danger."
    },
    {
        title: "Dowry Death Investigation",
        question: "Meera dies within two years of marriage under suspicious circumstances. Her in-laws claim suicide due to depression, but her family alleges dowry harassment. The autopsy is inconclusive. What does Section 304B IPC provide?",
        options: [
            "Burden of proof remains on prosecution to prove dowry death",
            "Presumption of dowry death - burden shifts to accused to prove innocence (Correct)",
            "Automatic conviction if death occurs within 7 years of marriage",
            "Only applies if dowry demands are proven independently"
        ],
        correct: 1,
        explanation: "Section 304B creates a presumption of dowry death when a woman dies unnaturally within 7 years of marriage and was subjected to dowry harassment. The burden shifts to the accused to prove their innocence - a significant departure from normal criminal law principles.",
        hint: "Section 304B IPC - Dowry death, Section 113B Evidence Act - Presumption",
        caselaw: "Biswajit Halder vs. State of West Bengal - Supreme Court clarified the scope of presumption under Section 304B."
    },
    {
        title: "Criminal Conspiracy",
        question: "Four college friends plan to cheat in exams by bribing the supervisor. They meet, discuss the plan, and collect ₹20,000. Before execution, Dev withdraws. The other three proceed but are caught. What is Dev's liability?",
        options: [
            "No liability as he withdrew before execution",
            "Full liability under Section 120B - conspiracy is complete upon agreement (Correct)",
            "Partial liability - guilty of attempt only",
            "Immunity if he cooperates with investigation"
        ],
        correct: 1,
        explanation: "Section 120B IPC - Criminal conspiracy is complete when two or more persons agree to do an illegal act. Withdrawal after agreement doesn't absolve liability for the conspiracy itself, though it may be considered during sentencing.",
        hint: "Section 120A defines conspiracy, 120B provides punishment",
        caselaw: "Kehar Singh vs. State - Conspiracy is complete upon agreement, subsequent withdrawal doesn't negate initial liability."
    },
    {
        title: "Kidnapping vs. Abduction",
        question: "A 16-year-old girl, Kavya, voluntarily leaves home to live with her 25-year-old boyfriend against her parents' wishes. Her parents file a kidnapping complaint. What are the legal issues?",
        options: [
            "No offense as Kavya went voluntarily",
            "Abduction under Section 362 as she was induced to go",
            "Kidnapping from lawful guardianship under Section 361 (Most appropriate)",
            "Both kidnapping and abduction charges apply"
        ],
        correct: 2,
        explanation: "Section 361 IPC - Kidnapping from lawful guardianship applies when a minor (under 16 for girls, 18 for boys) is taken from lawful guardian's custody, even with consent. Kavya's consent is irrelevant as she's below the age of consent for this purpose.",
        hint: "Key ages: Girls under 16, boys under 18 for kidnapping from guardianship",
        caselaw: "State of Haryana vs. Raja Ram - Minor's consent is irrelevant in kidnapping from lawful guardianship cases."
    },
    {
        title: "Attempt to Commit Murder",
        question: "Ramesh fires a gun at his business rival Sunil with intent to kill, but misses and only injures Sunil's arm. The bullet was aimed at Sunil's chest. Ramesh argues he should only be charged with causing hurt. What is the correct legal position?",
        options: [
            "Section 322 IPC - Voluntarily causing hurt (actual result)",
            "Section 307 IPC - Attempt to murder (intent-based charge) (Correct)",
            "Section 304 IPC - Culpable homicide (reduced charge)",
            "Section 325 IPC - Voluntarily causing grievous hurt"
        ],
        correct: 1,
        explanation: "Section 307 IPC - Attempt to murder applies when there's intent to kill and an overt act towards that goal. The actual result (hurt) is irrelevant if the intent was to kill and the act was likely to cause death. Aiming at chest shows intent to kill.",
        hint: "Attempt crimes focus on intention and overt act, not just the result",
        caselaw: "Om Prakash vs. State of Punjab - Attempt to murder depends on intention and nature of act, not just the actual injury caused."
    },
    {
        title: "Joint Liability in Rioting",
        question: "During a communal riot, 50 people attack shops. Most shout slogans, five throw stones, and two set fire to a shop. How should different participants be charged?",
        options: [
            "All 50 equally liable for all acts committed",
            "Differentiated liability based on individual acts (Most appropriate)",
            "Only the two who set fire are liable for serious charges",
            "All liable for rioting, none for individual acts"
        ],
        correct: 1,
        explanation: "Section 149 IPC creates joint liability for unlawful assembly, but individual acts require separate charges. All 50 liable for rioting (Section 147), stone-throwers additionally for mischief, arsonists for Section 435 (mischief by fire). Joint liability has limits based on common object.",
        hint: "Sections 141-160 deal with unlawful assembly and rioting",
        caselaw: "Masalti vs. State of UP - Supreme Court clarified limits of joint liability under Section 149 IPC."
    },
    {
        title: "Cyber Defamation",
        question: "Rohit posts false allegations on social media claiming his neighbor Anjali is having an extramarital affair. The post goes viral in their locality, damaging Anjali's reputation. What laws apply?",
        options: [
            "Only Section 499 IPC - Traditional defamation law",
            "Only IT Act 2000 - Cyber-specific provisions",
            "Both Section 499 IPC and Section 67 IT Act (Most comprehensive)",
            "Civil defamation suit only - no criminal liability"
        ],
        correct: 2,
        explanation: "Both laws apply: Section 499 IPC covers defamation generally, while Section 67 IT Act specifically addresses obscene/defamatory content in electronic form. The IT Act provides additional remedies and jurisdiction for online defamation cases.",
        hint: "IT Act 2000 supplements IPC for cyber crimes, doesn't replace it",
        caselaw: "Shreya Singhal vs. Union of India - Supreme Court guidelines on online speech and defamation."
    },
    {
        title: "Workplace Sexual Harassment",
        question: "Senior manager Mr. Sharma makes unwelcome sexual advances toward subordinate Ms. Verma, including inappropriate touching. When rejected, he threatens termination and gives negative reviews. What criminal charges apply?",
        options: [
            "Only Sexual Harassment at Workplace Act 2013 (civil remedy)",
            "Section 354 IPC - Assault/criminal force to outrage modesty",
            "Section 354A IPC - Sexual harassment (Most appropriate)",
            "All of the above - multiple legal remedies available"
        ],
        correct: 3,
        explanation: "Multiple remedies available: Section 354A IPC (sexual harassment), Section 354 IPC (outraging modesty through touching), and Sexual Harassment at Workplace Act 2013 (civil remedies, inquiry, compensation). Criminal and civil remedies can be pursued simultaneously.",
        hint: "2013 Act provides workplace-specific remedies; IPC provides criminal sanctions",
        caselaw: "Vishakha vs. State of Rajasthan - Foundation for workplace sexual harassment law in India."
    }
];

let currentQuestion = 0;
let selectedAnswer = null;
let score = 0;
let answered = false;
let startTime = Date.now();
let timerInterval;

function initializeQuiz() {
    currentQuestion = 0;
    score = 0;
    selectedAnswer = null;
    answered = false;
    startTime = Date.now();
    startTimer();
    displayQuestion();
    updateProgress();
}

function startQuiz() {
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('quizScreen').style.display = 'block';
    initializeQuiz();
}

function startTimer() {
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        document.getElementById('timer').innerHTML = 
            `⏱️ ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function displayQuestion() {
    const question = questions[currentQuestion];
    
    document.getElementById('questionCounter').textContent = 
        `Question ${currentQuestion + 1} of ${questions.length}`;
    
    document.getElementById('questionCard').innerHTML = `
        <div class="question-title">${question.title}</div>
        <div class="question-text">${question.question}</div>
        <div class="ipc-hint"><strong>Hint:</strong> ${question.hint}</div>
    `;
    
    const optionsContainer = document.getElementById('answerOptions');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.textContent = option;
        button.onclick = () => selectAnswer(index);
        optionsContainer.appendChild(button);
    });
    
    selectedAnswer = null;
    answered = false;
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('submitBtn').style.display = 'inline-block';
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('nextBtn').disabled = true;
    document.getElementById('prevBtn').disabled = currentQuestion === 0;
}

function selectAnswer(index) {
    if (answered) return;
    
    selectedAnswer = index;
    
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach((btn, idx) => {
        btn.classList.remove('selected');
        if (idx === index) {
            btn.classList.add('selected');
        }
    });
    
    document.getElementById('submitBtn').disabled = false;
}

function submitAnswer() {
    if (selectedAnswer === null || answered) return;
    
    answered = true;
    const question = questions[currentQuestion];
    const buttons = document.querySelectorAll('.option-btn');
    
    buttons.forEach((btn, index) => {
        btn.onclick = null;
        if (index === question.correct) {
            btn.classList.add('correct');
        } else if (index === selectedAnswer && index !== question.correct) {
            btn.classList.add('incorrect');
        }
    });
    
    if (selectedAnswer === question.correct) {
        score++;
    }
    
    const explanationDiv = document.getElementById('explanation');
    explanationDiv.innerHTML = `
        <div class="explanation-title">📚 Legal Analysis</div>
        <p><strong>Correct Answer:</strong> ${question.options[question.correct]}</p>
        <p><strong>Explanation:</strong> ${question.explanation}</p>
        <div class="case-law"><strong>Case Law:</strong> ${question.caselaw}</div>
    `;
    explanationDiv.style.display = 'block';
    
    document.getElementById('submitBtn').style.display = 'none';
    document.getElementById('nextBtn').disabled = false;
    
    if (currentQuestion === questions.length - 1) {
        document.getElementById('nextBtn').textContent = 'View Results →';
    }
}

function nextQuestion() {
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        displayQuestion();
        updateProgress();
        document.getElementById('submitBtn').style.display = 'inline-block';
        document.getElementById('nextBtn').textContent = 'Next →';
    } else {
        showResults();
    }
}

function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        displayQuestion();
        updateProgress();
        document.getElementById('submitBtn').style.display = 'inline-block';
        document.getElementById('nextBtn').textContent = 'Next →';
    }
}

function updateProgress() {
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
}

function showResults() {
    clearInterval(timerInterval);
    
    document.getElementById('quizScreen').style.display = 'none';
    document.getElementById('resultsScreen').style.display = 'block';
    
    const percentage = Math.round((score / questions.length) * 100);
    document.getElementById('scoreCircle').textContent = `${score}/${questions.length}`;
    
    let analysis = '';
    if (percentage >= 80) {
        analysis = `<h3 style="color: #6ee7b7;">Excellent! 🏆</h3>
                   <p>You have a strong understanding of Indian Criminal Law. You're well-prepared for practice!</p>`;
        document.getElementById('scoreCircle').style.background = 'linear-gradient(135deg, #10b981, #16a34a)';
    } else if (percentage >= 60) {
        analysis = `<h3 style="color: #c4b5fd;">Good Job! 👍</h3>
                   <p>Solid foundation in criminal law. Review the questions you missed to strengthen your knowledge.</p>`;
        document.getElementById('scoreCircle').style.background = 'linear-gradient(135deg, #a855f7, #8b5cf6)';
    } else {
        analysis = `<h3 style="color: #fca5a5;">Keep Studying! 📚</h3>
                   <p>You need more practice with IPC provisions and case law. Focus on the core principles and landmark judgments.</p>`;
        document.getElementById('scoreCircle').style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
    }
    document.getElementById('scoreAnalysis').innerHTML = analysis;
}

function restartQuiz() {
    document.getElementById('resultsScreen').style.display = 'none';
    document.getElementById('startScreen').style.display = 'block';
}

// Initial call to hide quiz screen and show start screen
window.onload = function() {
    document.getElementById('quizScreen').style.display = 'none';
    document.getElementById('resultsScreen').style.display = 'none';
};




























































































































































































































































