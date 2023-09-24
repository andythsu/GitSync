def get_problem_set_question_list_query():
    return """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
    total: totalNum
    questions: data {
      questionId
      title
      titleSlug
      content
      difficulty
      questionFrontendId
    }
  }
}
"""

def get_submission_list_query():
    return """
query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: Int, $status: Int) {
  questionSubmissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug, lang: $lang, status: $status) {
    lastKey
    hasNext
    submissions {
      id
      title
      titleSlug
      status
      statusDisplay
      lang
      langName
      runtime
      timestamp
      url
      isPending
      memory
      hasNotes
      notes
      flagType
      topicTags {
        id
      }
    }
  }
}
"""

def get_submission_details_query():
    return """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    runtime
    runtimeDisplay
    runtimePercentile
    runtimeDistribution
    memory
    memoryDisplay
    memoryPercentile
    memoryDistribution
    code
    timestamp
    statusCode
    lang {
      name
      verboseName
    }
    question {
      questionId
      title
      titleSlug
      content
      difficulty
      questionFrontendId
    }
    notes
    topicTags {
        tagId
        slug
        name
    }
    runtimeError
  }
}
"""
def get_user_status_query():
    return """
query globalData {
    userStatus {
      userId
    isSignedIn
    isMockUser
    isPremium
    isVerified
    username
    avatar
    isAdmin
    isSuperuser
    permissions
    isTranslator
    activeSessionId
    checkedInToday
    notificationStatus {
        lastModified
      numUnread
    }
  }
}
"""
