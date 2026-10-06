const task =
    document.getElementById("task");

const input =
    document.getElementById("inputText");

const submit =
    document.getElementById("submitBtn");

const buttonText =
    document.getElementById("buttonText");

const spinner =
    document.getElementById("spinner");

const result =
    document.getElementById("result");

const resultTitle =
    document.getElementById("resultTitle");

const errorBox =
    document.getElementById("error");

const copyBtn =
    document.getElementById("copyBtn");

const sampleBtn =
    document.getElementById("sampleBtn");


const samples = {

    qa:
        "What is the difference between RAM and ROM?",

    explain:
        "Explain the Pythagoras theorem for a beginner with a simple example.",

    quiz:
        `Photosynthesis is the process by which green plants use sunlight, carbon dioxide, and water to produce glucose and oxygen. Chlorophyll absorbs light energy needed for this process.`,

    summarize:
        `Artificial intelligence is a field of computer science that develops systems capable of performing tasks that normally require human intelligence. These tasks include learning, reasoning, language understanding, perception, and decision making. Modern AI systems can learn patterns from large datasets and use those patterns to make predictions or generate content.`,

    learn:
        "Python programming for a first-year engineering student"

};


task.addEventListener(
    "change",
    function () {

        input.placeholder =
            samples[task.value];

    }
);


sampleBtn.addEventListener(
    "click",
    function () {

        input.value =
            samples[task.value];

    }
);


submit.addEventListener(
    "click",
    async function () {

        const text =
            input.value.trim();


        if (!text) {

            showError(
                "Please enter a question, topic, or passage."
            );

            return;

        }


        setLoading(true);

        hideError();

        resultTitle.textContent =
            "Generating your result...";

        result.className =
            "result";

        result.innerHTML = "";

        copyBtn.classList.add(
            "hidden"
        );


        const endpoint =
            task.value === "learn"
                ? "/learn/recommendations"
                : `/${task.value}`;


        try {

            const response =
                await fetch(
                    endpoint,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Request failed."
                );

            }


            renderResult(
                data.task,
                data.result
            );


            copyBtn.classList.remove(
                "hidden"
            );


        } catch (error) {

            resultTitle.textContent =
                "Something went wrong";

            showError(
                error.message
            );

            result.className =
                "result empty";

            result.innerHTML =
                "<p>Check your API key and server, then try again.</p>";

        } finally {

            setLoading(false);

        }

    }
);


copyBtn.addEventListener(
    "click",
    async function () {

        const text =
            result.innerText;

        await navigator.clipboard
            .writeText(text);

        copyBtn.textContent =
            "Copied";

        setTimeout(
            function () {

                copyBtn.textContent =
                    "Copy";

            },
            1200
        );

    }
);


function setLoading(value) {

    submit.disabled =
        value;

    buttonText.textContent =
        value
            ? "Working..."
            : "Generate";

    spinner.classList.toggle(
        "hidden",
        !value
    );

}


function showError(message) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


function hideError() {

    errorBox.classList.add(
        "hidden"
    );

}


function renderResult(
    type,
    data
) {

    const titles = {

        qa: "Answer",

        explain:
            "Simple Explanation",

        quiz:
            "Practice Quiz",

        summarize:
            "Summary",

        learn:
            "Personalized Learning Path"

    };


    resultTitle.textContent =
        titles[type] || "Result";


    result.className =
        "result";


    if (type === "quiz") {

        renderQuiz(data);

        return;

    }


    if (type === "learn") {

        renderPath(data);

        return;

    }


    const pre =
        document.createElement(
            "pre"
        );


    pre.textContent =
        data;


    result.appendChild(pre);

}


function renderQuiz(data) {

    data.questions.forEach(
        function (question, index) {

            const box =
                document.createElement(
                    "div"
                );


            box.className =
                "quiz-question";


            const title =
                document.createElement(
                    "h4"
                );


            title.textContent =
                `${index + 1}. ${question.question}`;


            box.appendChild(title);


            question.options.forEach(
                function (option) {

                    const optionElement =
                        document.createElement(
                            "div"
                        );


                    optionElement.className =
                        "quiz-option";


                    optionElement.textContent =
                        option;


                    box.appendChild(
                        optionElement
                    );

                }
            );


            const answer =
                document.createElement(
                    "p"
                );


            answer.innerHTML =
                `<strong>Answer:</strong>
                ${escapeHtml(question.correct_answer)}
                <br>
                <small>
                ${escapeHtml(question.explanation || "")}
                </small>`;


            box.appendChild(
                answer
            );


            result.appendChild(
                box
            );

        }
    );

}


function renderPath(data) {

    const intro =
        document.createElement(
            "div"
        );


    intro.innerHTML =
        `<p>
            <strong>Goal:</strong>
            ${escapeHtml(data.goal || "")}
        </p>`;


    result.appendChild(
        intro
    );


    (data.stages || []).forEach(
        function (stage) {

            const box =
                document.createElement(
                    "div"
                );


            box.className =
                "path-stage";


            box.innerHTML = `

                <h4>
                    ${escapeHtml(stage.level)}
                    ·
                    ${escapeHtml(stage.duration || "")}
                </h4>

                <p>
                    <strong>Topics:</strong>
                    ${escapeHtml(
                        (stage.topics || []).join(", ")
                    )}
                </p>

                <p>
                    <strong>Practice:</strong>
                    ${escapeHtml(
                        (stage.practice || []).join(" • ")
                    )}
                </p>

                <p>
                    <strong>Resources:</strong>
                    ${escapeHtml(
                        (stage.resources || []).join(" • ")
                    )}
                </p>

            `;


            result.appendChild(
                box
            );

        }
    );


    if (
        data.study_tips &&
        data.study_tips.length
    ) {

        const tips =
            document.createElement(
                "p"
            );


        tips.innerHTML =
            `<strong>Study tips:</strong>
            ${escapeHtml(
                data.study_tips.join(" • ")
            )}`;


        result.appendChild(
            tips
        );

    }

}


function escapeHtml(value) {

    return String(value)
        .replace(
            /[&<>"']/g,
            function (character) {

                const entities = {

                    "&": "&amp;",

                    "<": "&lt;",

                    ">": "&gt;",

                    '"': "&quot;",

                    "'": "&#039;"

                };


                return entities[
                    character
                ];

            }
        );

}