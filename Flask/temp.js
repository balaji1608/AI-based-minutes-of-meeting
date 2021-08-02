
// function submit() {
//     console.log("Inside function");
//     var req =  fetch('http://localhost:5000/test', {
//         method: 'post',
//         body: "Tejas", 
//       }).then(res=>res.json());
//     req.then(result=> console.log(result));
// }

const summary = document.getElementById('summary')

function submit() {
    var ip = document.getElementById('input1')
    var req =  fetch('http://localhost:5000/youtube/', {
        method: 'post',
        body: ip.value, 
        responseType : 'blob'
      })
    var result = req.then(response=>response.text()).then(result=>
        {
            text = result
            var req = new XMLHttpRequest();
            req.open("POST", "http://localhost:5000/downloadfile/" + text , true);
            req.responseType = "blob";
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.onreadystatechange = function(){
            if (this.readyState == 4 && this.status == 200){
                var blob = new Blob([this.response], {type: "application/pdf"});
                var url = window.URL.createObjectURL(blob);
                var link = document.createElement('a');
                document.body.appendChild(link);
                link.style = "display: none";
                link.href = url;
                link.download = "minutes_of_meeting.pdf";
                link.click();

                setTimeout(() => {
                window.URL.revokeObjectURL(url);
                link.remove(); } , 100);
            }
    };
    req.send();
    })
}




function convertAudio(){
    audio  = new Audio('/home/tejas/Projects/EDI-2/Flask/static/test.wav')
    var req =  fetch('http://localhost:5000/audio/', {
        method: 'post',
        body: audio
      })
}



// to download pdf

function generatePdf(){
    var req = new XMLHttpRequest();
    var text ="Hello this is Balaji Pado from the team's parking newbies with my teammates exam Pareek and Kishan Pathani and not topic for project is sentiment analysis of covid-19 tweets visualisation dashpot. So this is the URL of a project which is made using flask and other tools so my want to the first tape that it takes so here person can manually type in the sentiment of any other statements and then there is a prediction of that statement whether it is positive or negative so let's. Let's I am Corona positive patients see the statement is actually negative and it is also the negative symbol is it means that this model is a having a good accuracy and prediction by this modern is of symmetry near 200 which is a good score. So what we are doing in next part is that we are scraping live tweets and then will predict the sentiment of those trips. So how will do that is will search for covid-19 tweets will scrape the twits and Infratech and we can see there are three sections the tweet the time and date and the sentiment of the twits. So here we have also add add one more unique feature that is text to audio so it will convert the result in audio. Let's scraper life that we can see it that way it is script this is a live to it and will when will click on text to audio will use gtts and the same script to it will be converted to audio order food. In terms of the Desolation part it consists of the live graph graph update daily on clicking the refresh button. Once you click the refresh button the code runs in the back and forth in the grass is updated on completely remove wrinkles on the screen the dashboard is displayed of debit card on refreshing as I have clicked this it would show the live updates itself and now you can see that the life graphics. silvarpatti of the negative reactions of the people that is negative weight while the golden path is of depositing and there in this graph the Blue button positive with the red part  var text ="Hello this is Balaji Pado from the team's parking newbies with my teammates exam Pareek and Kishan Pathani and not topic for project is sentiment analysis of covid-19 tweets visualisation dashpot. So this is the URL of a project which is made using flask and other tools so my want to the first tape that it takes so here person can manually type in the sentiment of any other statements and then there is a prediction of that statement whether it is positive or negative so let's. Let's I am Corona positive patients see the statement is actually negative and it is also the negative symbol is it means that this model is a having a good accuracy and prediction by this modern is of symmetry near 200 which is a good score. So what we are doing in next part is that we are scraping live tweets and then will predict the sentiment of those trips. So how will do that is will search for covid-19 tweets will scrape the twits and Infratech and we can see there are three sections the tweet the time and date and the sentiment of the twits. So here we have also add add one more unique feature that is text to audio so it will convert the result in audio. Let's scraper life that we can see it that way it is script this is a live to it and will when will click on text to audio will use gtts and the same script to it will be converted to audio order food. In terms of the Desolation part it consists of the live graph graph update daily on clicking the refresh button. Once you click the refresh button the code runs in the back and forth in the grass is updated on completely remove wrinkles on the screen the dashboard is displayed of debit card on refreshing as I have clicked this it would show the live updates itself and now you can see that the life graphics. silvarpatti of the negative reactions of the people that is negative weight while the golden path is of depositing and there in this graph the Blue button positive with the red part is for the negative it. In this dashboard Park again this is the mode It is there is the difference of whs dashboard and the billiard sentence about us and it also contains the contact us feature and also our profile of various social media effect. This whole web page is designed using the HTML as well as the part which book particularly is the contribution in our project by that member. So this is all about of sentiment analysis project. Thank you "is for the negative it. In this dashboard Park again this is the mode It is there is the difference of whs dashboard and the billiard sentence about us and it also contains the contact us feature and also our profile of various social media effect. This whole web page is designed using the HTML as well as the part which book particularly is the contribution in our project by that member. So this is all about of sentiment analysis project. Thank you "
    req.open("POST", "http://localhost:5000/downloadfile/" + text , true);
    req.responseType = "blob";
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
        var blob = new Blob([this.response], {type: "application/pdf"});
        var url = window.URL.createObjectURL(blob);
        var link = document.createElement('a');
        document.body.appendChild(link);
        link.style = "display: none";
        link.href = url;
        link.download = "minutes_of_meeting.pdf";
        link.click();

        setTimeout(() => {
        window.URL.revokeObjectURL(url);
        link.remove(); } , 100);
    }
    };
    req.send();
}