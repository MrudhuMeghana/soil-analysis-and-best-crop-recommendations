document.getElementById("crop-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (result.success) {
            // Display recommendations with images
            const recommendations = result.recommendations;
            const cropImages = ["crop1-img", "crop2-img", "crop3-img"];
            const cropConfidences = ["crop1-confidence", "crop2-confidence", "crop3-confidence"];

            recommendations.forEach((rec, index) => {
                const cropImage = document.getElementById(cropImages[index]);
                const cropConfidence = document.getElementById(cropConfidences[index]);

                // Set the image source dynamically
                cropImage.src = `/static/${rec.crop}.jpeg`;
                cropConfidence.textContent = `${rec.crop}: ${rec.probability}% Confidence`;
            });

            // Scroll to recommendations section
            document.getElementById("recommendations").scrollIntoView({ behavior: "smooth" });
        } else {
            alert("Error: " + result.error);
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
    }
});
document.getElementById("feedback-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent the form from reloading the page

    const feedback = document.getElementById("feedback-text").value;

    try {
        const response = await fetch("/feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ feedback }),
        });

        const result = await response.json();

        if (result.success) {
            alert("Thank you for your feedback!");
            document.getElementById("feedback-text").value = ""; // Clear the textarea
        } else {
            alert("Error: " + result.error);
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
    }
});