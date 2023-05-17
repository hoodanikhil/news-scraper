// static/script.js
$(document).ready(function() {
    $("#myForm").submit(function(event) {
        event.preventDefault();
        const inputText = $("#myTextField").val();
        const numArticles = $("#numArticlesField").val();
        $("#loadingMessage").show(); // Show the loading message
        $.post("/button", { text: inputText, num_articles: numArticles }, function(data) {
            let articles = data.result.map(article => {
                let bodyText = article.description ? article.description : "";
                let dateString = article.date_publish? (new Date(article.date_publish)).toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }) : "";
                return `
                <div class="card mb-4">
                    <div class="row no-gutters">
                        <div class="col-md-4">
                            <img src="${article.image_url}" class="card-img" alt="${article.headline}">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title"><a href="${article.article_url}" target="_blank">${article.headline} - ${article.source}</a></h5>
                                <p class="card-title"><small class="text-muted">${dateString}</small></p>
                                <p class="card-text">${bodyText}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;});
            $("#resultList").empty().append(articles.join(''));
        }).always(function() {
            $("#loadingMessage").hide(); // Hide the loading message
        });
    });
});
