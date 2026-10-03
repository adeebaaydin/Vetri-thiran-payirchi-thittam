document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "#planner-form"
            );


        if (!form) {
            return;
        }


        const path =
            location.pathname;


        const planner =
            path.split("/").pop();


        const results =
            document.querySelector(
                "#results"
            );


        form.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                results.innerHTML =
                    `
                    <div class="empty">
                        Thinking and building
                        your plan…
                    </div>
                    `;


                let options = {
                    method: "POST"
                };


                if (planner === "jewelry") {

                    options.body =
                        new FormData(form);

                } else {

                    const formData =
                        new FormData(form);

                    const payload = {};


                    formData.forEach(
                        (value, key) => {

                            if (
                                key === "rooms"
                            ) {

                                payload.rooms =
                                    String(value)
                                        .split(",")
                                        .map(
                                            item =>
                                                item.trim()
                                        )
                                        .filter(
                                            Boolean
                                        );

                            }

                            else if (
                                key === "budget"
                                ||
                                key === "guests"
                            ) {

                                payload[key] =
                                    Number(value);

                            }

                            else {

                                payload[key] =
                                    value;
                            }

                        }
                    );


                    options.headers = {
                        "Content-Type":
                            "application/json"
                    };


                    options.body =
                        JSON.stringify(
                            payload
                        );
                }


                const endpoint =
                    "/api/generate-" +
                    planner;


                try {

                    const response =
                        await fetch(
                            endpoint,
                            options
                        );


                    const data =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Request failed"
                        );

                    }


                    renderResults(
                        data
                    );

                }

                catch (error) {

                    results.innerHTML =
                        `
                        <div class="error">
                            ${
                                escapeHtml(
                                    error.message
                                )
                            }
                        </div>
                        `;

                }

            }
        );


        function renderResults(data) {

            const allocations =
                Object.entries(
                    data.budget_allocation ||
                    {}
                )
                .map(
                    ([key, value]) =>
                        `
                        <div>
                            <strong>
                                ${
                                    escapeHtml(
                                        key
                                    )
                                }
                            </strong>

                            <br>

                            ₹${
                                Number(value)
                                .toLocaleString(
                                    "en-IN"
                                )
                            }
                        </div>
                        `
                )
                .join("");


            const recommendations =
                (
                    data.recommendations ||
                    []
                )
                .map(
                    recommendation =>
                        `
                        <article class="rec">

                            <div class="rec-top">

                                <strong>
                                    ${
                                        escapeHtml(
                                            recommendation.title
                                        )
                                    }
                                </strong>

                                <span class="price">

                                    ₹${
                                        Number(
                                            recommendation
                                                .estimated_price
                                        )
                                        .toLocaleString(
                                            "en-IN"
                                        )
                                    }

                                </span>

                            </div>


                            <p>
                                ${
                                    escapeHtml(
                                        recommendation
                                            .description
                                    )
                                }
                            </p>


                            <small>

                                ${
                                    escapeHtml(
                                        recommendation
                                            .category
                                    )
                                }

                                ·

                                ${
                                    escapeHtml(
                                        recommendation
                                            .platform
                                    )
                                }

                            </small>


                            <p>

                                <b>
                                    Why:
                                </b>

                                ${
                                    escapeHtml(
                                        recommendation
                                            .why_it_fits
                                    )
                                }

                            </p>


                            <a
                                href="${
                                    safeUrl(
                                        recommendation
                                            .search_url
                                    )
                                }"
                                target="_blank"
                                rel="noopener noreferrer"
                            >

                                Search on
                                ${
                                    escapeHtml(
                                        recommendation
                                            .platform
                                    )
                                }
                                →

                            </a>

                        </article>
                        `
                )
                .join("");


            const tips =
                (
                    data.tips ||
                    []
                )
                .map(
                    tip =>
                        `
                        <li>
                            ${
                                escapeHtml(
                                    tip
                                )
                            }
                        </li>
                        `
                )
                .join("");


            results.innerHTML =
                `
                <div class="result-header">

                    <span class="eyebrow">

                        ${
                            escapeHtml(
                                data.planner
                            )
                        }

                        PLAN

                    </span>


                    <h2>

                        ${
                            escapeHtml(
                                data.summary
                            )
                        }

                    </h2>


                    <div class="alloc">

                        ${allocations}

                    </div>


                    <small>

                        ${
                            data.ai_used
                                ? "Generated with Gemini"
                                : "Fallback/demo recommendations"
                        }

                    </small>

                </div>


                <h3>
                    Recommendations
                </h3>


                ${recommendations}


                <div class="tips">

                    <b>
                        Tips
                    </b>


                    <ul>
                        ${tips}
                    </ul>

                </div>
                `;
        }


        function escapeHtml(value) {

            return String(
                value ?? ""
            ).replace(
                /[&<>"']/g,
                character => {

                    const entities = {

                        "&": "&amp;",
                        "<": "&lt;",
                        ">": "&gt;",
                        '"': "&quot;",
                        "'": "&#39;"

                    };

                    return entities[
                        character
                    ];

                }
            );

        }


        function safeUrl(value) {

            try {

                const url =
                    new URL(
                        value,
                        location.origin
                    );


                if (
                    url.protocol === "http:"
                    ||
                    url.protocol === "https:"
                ) {

                    return url.href;

                }


                return "#";

            }

            catch {

                return "#";

            }

        }

    }
);