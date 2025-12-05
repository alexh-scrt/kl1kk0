import { json, type RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json().catch(() => ({}));
	const prompt = typeof body?.prompt === 'string' ? body.prompt : '';

	return json({
		reply: prompt
			? `Stub: Received "${prompt}". Connect this route to your LLM backend.`
			: 'Stub: Ready for LLM hookup.'
	});
};
