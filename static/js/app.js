const $ = (s) => document.querySelector(s);

const esc = (v) =>
  String(v ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");

function asArray(value) {
  if (Array.isArray(value)) {
    return value;
  }

  if (value === null || value === undefined || value === "") {
    return [];
  }

  if (typeof value === "string") {
    return [value];
  }

  return [value];
}

function exerciseText(value) {
  if (typeof value === "string") {
    return esc(value);
  }

  if (!value || typeof value !== "object") {
    return esc(value);
  }

  return `${esc(value.name)} — ${esc(value.sets)} × ${esc(value.reps)} (${esc(value.rest)})`;
}

async function data(r) {
  const x = await r.json().catch(() => ({}));

  if (!r.ok) {
    throw Error(x.detail || "Request failed");
  }

  return x;
}

function message(el, t, c = "") {
  if (el) {
    el.textContent = t;
    el.className = "message " + c;
  }
}

function renderPlan(p) {
  // Summary
  $("#summary").innerHTML = `
    <div class="stat">
      <span>Goal</span>
      <strong>${esc(p.summary?.goal)}</strong>
    </div>

    <div class="stat">
      <span>Level</span>
      <strong>${esc(p.summary?.level)}</strong>
    </div>

    <div class="stat">
      <span>Frequency</span>
      <strong>${esc(p.summary?.frequency)}</strong>
    </div>
  `;

  // Weekly workout plan
  const weeklyPlan = asArray(p.weekly_plan);

  $("#days").innerHTML = weeklyPlan
    .map((d) => {
      const warmup = asArray(d?.warmup);
      const exercises = asArray(d?.exercises);
      const cooldown = asArray(d?.cooldown);

      return `
        <article class="card">

          <h3>
            ${esc(d?.day)} · ${esc(d?.workout_type)}
          </h3>

          <p>
            ${esc(d?.duration)} minutes
          </p>

          <b>Warm-up</b>

          <ul>
            ${warmup
              .map((x) => `<li>${esc(x)}</li>`)
              .join("")}
          </ul>

          <b>Exercises</b>

          <ul>
            ${exercises
              .map((x) => `<li>${exerciseText(x)}</li>`)
              .join("")}
          </ul>

          <b>Cool-down</b>

          <ul>
            ${cooldown
              .map((x) => `<li>${esc(x)}</li>`)
              .join("")}
          </ul>

        </article>
      `;
    })
    .join("");

  // Recovery
  $("#recovery").innerHTML = asArray(p.recovery)
    .map((x) => `<li>${esc(x)}</li>`)
    .join("");

  // Safety note
  $("#safety").textContent =
    p.safety_note ||
    "Consult a qualified professional for injuries or serious health concerns.";

  // Show results
  $("#results").classList.remove("hidden");

  $("#results").scrollIntoView({
    behavior: "smooth"
  });
}


// Store user profile for meal-plan generation
let profile = null;


// ==========================================
// FITNESS PLAN GENERATION
// ==========================================

$("#fitness-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const b = $("#generate");
  const f = new FormData(e.currentTarget);

  profile = Object.fromEntries(f);

  for (const k of [
    "age",
    "height",
    "weight",
    "workout_days",
    "duration"
  ]) {
    profile[k] = Number(profile[k]);
  }

  b.disabled = true;
  b.textContent = "Generating with Gemini...";

  message(
    $("#message"),
    "Creating your plan..."
  );

  try {
    const x = await data(
      await fetch("/api/generate-plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(profile)
      })
    );

    renderPlan(x.plan);

    message(
      $("#message"),
      "Plan generated.",
      "success"
    );

  } catch (err) {

    message(
      $("#message"),
      err.message,
      "error"
    );

  } finally {

    b.disabled = false;
    b.textContent = "Generate AI Fitness Plan";
  }
});


// ==========================================
// MEAL PLAN GENERATION
// ==========================================

$("#meals-btn")?.addEventListener("click", async () => {

  if (!profile) {
    return message(
      $("#meal-message"),
      "Generate a fitness plan first.",
      "error"
    );
  }

  try {

    const x = await data(
      await fetch("/api/generate-meal-plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          goal: profile.goal,
          level: profile.level,
          dietary_preference: profile.dietary_preference,
          weight: profile.weight,
          limitations: profile.limitations
        })
      })
    );

    const m = x.meal_plan || {};

    const mealTypes = [
      "breakfast",
      "lunch",
      "dinner",
      "snacks",
      "nutrition_tips"
    ];

    $("#meals").innerHTML = mealTypes
      .map((k) => {

        const items = asArray(m[k]);

        return `
          <article class="card">

            <h3>
              ${k.replace("_", " ")}
            </h3>

            <ul>
              ${items
                .map((v) => `<li>${esc(v)}</li>`)
                .join("")}
            </ul>

          </article>
        `;
      })
      .join("");

    message(
      $("#meal-message"),
      "Meal suggestions generated.",
      "success"
    );

  } catch (err) {

    message(
      $("#meal-message"),
      err.message,
      "error"
    );
  }
});


// ==========================================
// PROGRESS DASHBOARD
// ==========================================

async function loadProgress() {

  const x = await data(
    await fetch("/api/progress")
  );

  const r = x.records || [];

  // Total records
  $("#total-records").textContent = r.length;

  // Total completed workouts
  $("#total-workouts").textContent =
    r.filter((v) => v.workout_completed).length;

  // Current weight
  $("#current-weight").textContent =
    r.length
      ? Number(r.at(-1).weight).toFixed(1) + " kg"
      : "—";

  // History table
  $("#history").innerHTML = r.length
    ? r
        .slice()
        .reverse()
        .map(
          (v) => `
            <tr>
              <td>${esc(v.date)}</td>

              <td>
                ${Number(v.weight).toFixed(1)} kg
              </td>

              <td>
                ${v.workout_completed ? "Yes" : "No"}
              </td>

              <td>
                ${v.workout_duration} min
              </td>

              <td>
                ${esc(v.notes)}
              </td>
            </tr>
          `
        )
        .join("")
    : `
        <tr>
          <td colspan="5">
            No records yet.
          </td>
        </tr>
      `;

  // Weight chart
  if (window.Chart) {

    const canvas = $("#chart");

    if (canvas) {

      new Chart(canvas, {
        type: "line",

        data: {
          labels: r.map((v) => v.date),

          datasets: [
            {
              label: "Weight (kg)",

              data: r.map((v) => v.weight),

              tension: 0.3
            }
          ]
        }
      });
    }
  }
}


// ==========================================
// SAVE PROGRESS
// ==========================================

$("#progress-form")?.addEventListener(
  "submit",
  async (e) => {

    e.preventDefault();

    try {

      await data(
        await fetch("/api/progress", {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            date: $("#date").value,

            weight: Number(
              $("#weight").value
            ),

            workout_completed:
              $("#completed").value === "true",

            workout_duration:
              Number(
                $("#duration").value || 0
              ),

            notes:
              $("#notes").value
          })
        })
      );

      message(
        $("#progress-message"),
        "Progress saved.",
        "success"
      );

      e.currentTarget.reset();

      $("#date").value =
        new Date()
          .toISOString()
          .slice(0, 10);

      await loadProgress();

    } catch (err) {

      message(
        $("#progress-message"),
        err.message,
        "error"
      );
    }
  }
);


// ==========================================
// INITIALIZE PROGRESS PAGE
// ==========================================

if ($("#progress-form")) {

  $("#date").value =
    new Date()
      .toISOString()
      .slice(0, 10);

  loadProgress().catch(
    (e) =>
      message(
        $("#progress-message"),
        e.message,
        "error"
      )
  );
}