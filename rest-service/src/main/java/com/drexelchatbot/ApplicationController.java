package com.drexelchatbot;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

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
	public QueryResponse response(@RequestParam(value = "query", defaultValue = "") String query,
			HttpServletRequest request) {
		log.info("Responding to query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		log.info("Processing query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		Process cmdProc = null;
		String line = null;
		String ret = "";
		try {
			cmdProc = Runtime.getRuntime()
					.exec(new String[] { "python3", "./../chatbot/main.py", "\"" + query + "\"", "2>/dev/null" });

			BufferedReader stdoutReader = new BufferedReader(new InputStreamReader(cmdProc.getInputStream()));
			while ((line = stdoutReader.readLine()) != null) {
				// process standard output here
				System.out.println(line);
				if (line != null) {
					ret += line;
				}
			}

			BufferedReader stderrReader = new BufferedReader(new InputStreamReader(cmdProc.getErrorStream()));
			while ((line = stderrReader.readLine()) != null) {
				// process standard error here
				// System.out.println(line);
			}
			cmdProc.waitFor();
			int retValue = cmdProc.exitValue();
			cmdProc.destroy();
		} catch (IOException | InterruptedException e) {

			e.printStackTrace();
		}

		log.info("Returning for query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		return new QueryResponse(ret);
	}

}
