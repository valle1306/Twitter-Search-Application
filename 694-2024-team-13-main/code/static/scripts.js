document.getElementById('search-btn').addEventListener('click', function() {
    let query = document.getElementById('search-box').value;
    currentSearchType = 'query';  // 确保搜索类型是关键词
    currentSearchParam = query;  // 更新当前搜索参数

    currentPage = 1; // 重置为第一页
    fetch(`/search?query=${encodeURIComponent(query)}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'query=' + encodeURIComponent(query)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (Object.keys(data).length > 0) {
            displayResults(data, true);
        }
    }).catch(error => {
        console.error('Error:', error);
    });
});


function displayResults(data, clearContents) {
    let peopleContainer = document.getElementById('people-container');
    let tweetsContainer = document.getElementById('tweets-container');

    if (clearContents) {
        peopleContainer.innerHTML = '';
        tweetsContainer.innerHTML = '';
    }

    console.log('people')
    if (data.people) {
        // For each person, create a new div element and add it to peopleContainer
        data.people.forEach(function(person) {
            console.log(person)
            let personDiv = document.createElement('div');
            personDiv.className = 'person';
            personDiv.innerHTML = `
                <h4>${person.name} (@${person.screenName})</h4>
                <p>${person.followers}</p>`;

            peopleContainer.appendChild(personDiv);
        });
    }

    console.log('tweet')
    if (data.tweets) {
        // Create a new div element for each tweet and add it to tweetsContainer
        data.tweets.forEach(function(tweet) {
            let tweetDiv = document.createElement('div');
            tweetDiv.className = 'tweet';
            // Format the date and time
            let tweetDate = new Date(tweet.created_at.$date);
            let formattedDate = tweetDate.toLocaleString();

            // Construct the tweet link, assuming the tweet can be accessed through a standard URL format
            let tweetLink = `https://twitter.com/${tweet.user.screen_name}/status/${tweet.tweet_id.toString()}`;

            // 用户名单独处理，不包含在<a>标签内
            let userNameSpan = document.createElement('span');
            userNameSpan.className = 'user-name clickable';
            userNameSpan.textContent = `${tweet.user.name} (@${tweet.user.screen_name})`;
            userNameSpan.setAttribute('data-username', tweet.user.screen_name);
            userNameSpan.style.cursor = 'pointer'; // 显示为可点击
            userNameSpan.style.textDecoration = 'underline';
            userNameSpan.style.display = 'block'; // 使其表现为块级元素，占满整行
            userNameSpan.style.textAlign = 'left'; // 文本对齐到左边
            userNameSpan.style.marginRight = 'auto'; // 右边自动填充空间，左对齐


            // 添加点击事件
            userNameSpan.addEventListener('click', function(event) {
                event.preventDefault();  // 阻止默认行为，如链接跳转
                event.stopPropagation(); // 阻止事件冒泡

                currentSearchType = 'username';  // 更改搜索类型为用户名搜索
                currentSearchParam = this.getAttribute('data-username');  // 更新搜索参数为用户名

                fetchUserTweets(this.getAttribute('data-username'));
            });

            // 创建正常的推文链接部分
            let tweetContent = document.createElement('a');
            tweetContent.href = tweetLink;
            tweetContent.target = "_blank";
            tweetContent.style.textDecoration = "none";
            tweetContent.style.color = "inherit";
            tweetContent.innerHTML = `
                <p>${tweet.text}</p>
                <span>${formattedDate}</span>
            `;

            // 组装元素
            tweetDiv.appendChild(userNameSpan);
            tweetDiv.appendChild(tweetContent);
            tweetsContainer.appendChild(tweetDiv);
        });
    }
    console.log('done')
}

function fetchUserTweets(username) {
    console.log('fetch')
    currentPage = 1
    fetch(`/search_user_tweets?username=${encodeURIComponent(username)}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data, true); // 清空现有内容并显示新内容
        })
        .catch(error => {
            console.error('Error fetching user tweets:', error);
        });
}

// ...
// Current page and expected page size for loading tweets
let currentPage = 1;
const pageSize = 10;  // Assuming 10 tweets are loaded per page

let currentSearchType = 'query';  // 默认为关键词搜索
let currentSearchParam = '';      // 初始化搜索参数为空

// Listen for scroll events to load more tweets
window.addEventListener('scroll', () => {
    // Check if the user has scrolled to the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadMoreTweets(currentPage);
    }
});

function loadMoreTweets() {
    currentPage++;  // 递增页面
    let url = '';

    if (currentSearchType === 'query') {
        url = `/search?query=${encodeURIComponent(currentSearchParam)}&page=${currentPage}&pageSize=${pageSize}`;
    } else if (currentSearchType === 'username') {
        url = `/search_user_tweets?username=${encodeURIComponent(currentSearchParam)}&page=${currentPage}&pageSize=${pageSize}`;
    }

    fetch(url, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data && (data.people.length > 0 || data.tweets.length > 0)) {
                displayResults(data, false); // 追加新的结果到现有内容
            }
        }).catch(error => {
            console.error('Error loading more tweets:', error);
        });
}

