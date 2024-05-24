from langchain_core.prompts import PromptTemplate

class PromptTemplates:
    @staticmethod
    def question_answer_template(context_placeholder="{context}", question_placeholder="{question}"):
        """
        Generate a question-answer template.

        Args:
            context_placeholder (str): Placeholder for context in the prompt template.
            question_placeholder (str): Placeholder for question in the prompt template.

        Returns:
            PromptTemplate: Prompt template for question-answer.
        """
        prompt_template = f"""You are an AI teaching assistant designed to help students understand course material. 
          Your role is to provide clear, concise explanations tailored to the student's level of understanding based on the notes provided as context.
          Do not answer questions if they are not relevant to the context or discussion.
          Break down complex topics into easy-to-understand steps.
          Use examples and analogies to illustrate points.

        Context:
        {context_placeholder}?

        Question:
        {question_placeholder}

        Answer:
        """
        input_variables = ["context", "question"]
        return PromptTemplate(template=prompt_template, input_variables=input_variables)
    
    @staticmethod
    def chunks_summary_prompt_template():
        """
        Generate a prompt template for summarizing chunks of text.
        
        Returns:
            PromptTemplate: Prompt template for summarizing text chunks.
        """
        prompt_template = """
        Summarize the key points and main ideas from the given document in a clear and concise manner. 
        The summary should capture the essence of the content while omitting unnecessary details. 
        Focus on the most important information, major arguments, conclusions, and takeaways. 
        Present the summary in a well-structured format using complete sentences and proper paragraphs:
        document:`{text}'
        Summary:
        """
        return PromptTemplate(input_variables=['text'], template=prompt_template)
    
    @staticmethod
    def final_combine_summary_prompt_template():
        """
        Generate a prompt template for a final summary of an entire document.
        
        Returns:
            PromptTemplate: Prompt template for final document summary.
        """
        prompt_template = '''
        Organize the following summaries of chunks of text into a clear, coherent and well presented text.
        document: `{text}`
        '''
        return PromptTemplate(input_variables=['text'], template=prompt_template)
    
    @staticmethod
    def quiz_generation_prompt_template():
        """
        Generate a prompt template for generating a quiz.
        
        Returns:
            PromptTemplate: Prompt template for quiz generation.
        """
        template = """
          Text: {text}
          You are an expert MCQ maker. Given the above text, it is your job to \
          create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
          Make sure the questions are not repeated and check all the questions to be conforming the text as well.

        Example Questions:

        1. In the context of a study analyzing overfitting in statistical models, 
         when applying the concept of regularization in ridge linear regression, 
        which RBF network configuration is considered 'most regularized'?

             A. Small M and small λ
             B. Small M and large λ
            C. Large M and small λ
            D. Large M and large λ

         2. Given recent advances in machine learning, which statement is correct about selecting base learners for an ensemble when designing a system for predictive accuracy?
            A. Different learners can come from the same algorithm with varying hyperparameters
            B. Different learners can be based on different algorithms
            C. Different learners can utilize different training spaces
           D. All of the above


         3. Based on research findings in model diversity, which of the following statements are true regarding weak learners in ensemble models as related to enhancing ensemble performance?
             A. They have low variance and typically do not overfit
            B. They have high variance and usually overfit
            C. They have high bias and struggle with complex learning problems
            D. None of the above


          Make sure to format your response like RESPONSE_JSON below  and use it as a guide. \
          Ensure to make {number} MCQs
          ### RESPONSE_JSON
          {response_json}
          """
        return PromptTemplate(
            input_variables=["text", "number", "subject", "tone", "response_json"],
            template=template
        )
    
    @staticmethod
    def quiz_evaluation_prompt_template():
        """
        Generate a prompt template for evaluating a quiz.
        
        Returns:
            PromptTemplate: Prompt template for quiz evaluation.
        """
        template = """
        You are an expert Artificial Intelligence and Data science teacher. Given a Multiple Choice Quiz for {subject} students.\
        You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
        if the quiz is not at per with the cognitive and analytical abilities of the students,\
        update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
        Quiz_MCQs:
        {quiz}

        Check from an expert English Writer of the above quiz:
        """
        return PromptTemplate(
            input_variables=["subject", "quiz"],
            template=template
        )


