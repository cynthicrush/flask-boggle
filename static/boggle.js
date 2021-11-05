class Boggle {
  constructor() {
    this.score = 0;
    this.time = 61;
    this.words = new Set();
    this.timer = setInterval(this.countDown.bind(this), 1000);
    // this.board = $('.boggle')
    $(".new-word").on("submit", this.handleSubmit.bind(this));
  }

  showMessage(message) {
    $(".message").text(message);
  }

  showWord(word) {
    $(".words-list").append(`<li>${word}</li>`);
  }

  showScore() {
    $(".score").text(this.score);
  }

  showTimer() {
    $(".timer").text(this.time);
  }

  async countDown() {
    this.time -= 1;
    this.showTimer();

    if (this.time <= 0) {
      clearInterval(this.timer);
      $(".new-word").hide();
      this.showMessage(`Final score: ${this.score}`);
      await this.scorePoints()
    }
  }

  async handleSubmit(event) {
    event.preventDefault();

    const $word = $(".word");
    let word = $word.val();

    const $message = $(".message");

    if (this.words.has(word)) {
      return $message.text(`${word} is already in your list.`);
    }

    const response = await axios.get("/word-check", { params: { word: word } });
    if (response.data.result === "not-word") {
      this.showMessage(`${word} is not a valid English word.`);
    } else if (response.data.result === "not-on-board") {
      this.showMessage(`${word} is not a valid word on the game board.`);
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
    }

    $(".new-word")[0].reset();
  }

  async scorePoints() {
    $(".new-word").hide();
    const response = await axios.post('/post-score-times', {score: this.score})
    if(response.data.newRecord) {
      this.showMessage(`New record: ${this.score}`)
    } else {
      this.showMessage(`Your score: ${this.score}`)
    }
  }
}

// this.handleSubmit.bind(this)
