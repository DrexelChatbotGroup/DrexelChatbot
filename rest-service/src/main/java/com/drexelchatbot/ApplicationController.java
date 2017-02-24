package com.drexelchatbot;

import java.util.Random;

import javax.servlet.http.HttpServletRequest;

import org.apache.log4j.Logger;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApplicationController {
	Logger log = Logger.getLogger(ApplicationController.class);


	@RequestMapping(value = "/chatbot/api", method = RequestMethod.GET)
	public QueryResponse response(@RequestParam(value = "query", defaultValue = "") String name,
			HttpServletRequest request) {
		log.info("Responding to query: '" + name + "'" + " from remote IP " + request.getRemoteAddr());

		log.info("Processing query: '" + name + "'" + " from remote IP " + request.getRemoteAddr());

		log.info("Returning for query: '" + name + "'" + " from remote IP " + request.getRemoteAddr());

		return new QueryResponse(String.format("Responding to query: '" + name + "'"));
	}

}
