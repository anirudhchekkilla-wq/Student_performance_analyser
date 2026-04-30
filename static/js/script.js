const subjects = {
    "CSE": {
        1: ["Maths", "C", "English", "Chemistry"],
        2: ["DS", "Python", "Physics", "Maths2"],
        3: ["OOP", "Java", "DBMS", "OS"],
        4: ["CN", "CPP", "SE", "DM"],
        5: ["AI", "ML", "DL", "CV"],
        6: ["NLP", "Big Data", "Cloud", "Cyber Security"],
        7: ["IoT", "Blockchain", "Data Science", "Ethical Hacking"],
        8: ["Mobile App Dev", "Web Dev", "Software Testing", "Project Management"]
    },
    "IT": {
        1: ["Maths", "C", "English", "Chemistry"],
        2: ["DS", "Python", "Physics", "Maths2"],
        3: ["OOP", "QALR", "UHV", "DE"],
        4: ["CO", "ITWS", "DBMS", "PP"],
        5: ["DAA", "CN", "IDS", "DWDM", "IPR", "SE"],
        6: ["OS", "Big Data", "AIDL", "CSCL", "ML", "WT"],
        7: ["IoT", "Blockchain", "Data Science", "Ethical Hacking"],
        8: ["Mobile App Dev", "Web Dev", "Software Testing", "Project Management"]
    }
};

function subjectKey(sub) {
    return sub.replaceAll(" ", "_").replaceAll("-", "_").toLowerCase();
}

function loadSubjects() {
    const branch = document.getElementById("branch").value;
    const sem = document.getElementById("semester").value;
    const container = document.getElementById("subjects-container");

    if (!container) return;

    container.innerHTML = "";

    if (subjects[branch] && subjects[branch][sem]) {
        subjects[branch][sem].forEach(sub => {
            const key = subjectKey(sub);

            container.innerHTML += `
                <div class="subject-row">
                    <div>
                        <label class="subject-name">${sub}</label>
                    </div>
                    <div>
                        <label>Internal</label>
                        <input name="${key}_internal" type="number" min="0" max="40" required>
                    </div>
                    <div>
                        <label>External</label>
                        <input name="${key}_external" type="number" min="0" max="60" required>
                    </div>
                </div>
            `;
        });
    }
}