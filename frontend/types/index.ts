export interface IAPIResponse<T> {
	data: T;
	message: string;
	status: number;
}

export interface IProfileResponse {
	username: string;
	email: string;
	user_fullname: string;
	user_role: string;
	created_at: string;
	updated_at: string;
}

export interface ILoginFormValues {
	username: string;
	password: string;
}

export interface IUser {
	username: string;
	email: string;
	user_fullname: string;
	user_role: string;
	created_at: string;
	updated_at: string;
}

export interface IRegisterFormValues {
	username: string;
	email: string;
	password: string;
	user_fullname: string;
}

export interface IRegisterResponse {
	username: string;
	email: string;
	user_fullname: string;
}

export interface IChatBotResponse {
	id: string;
	user_id: string;
	name: string;
	config: string;
	status: string;
	created_at: string;
	updated_at: string;
}

export interface IConversationResponse {
	id: string;
	chatbot_id: string;
	user_id: string;
	created_at: string;
	updated_at: string;
}

export interface IMessageResponse {
	id: string;
	conversation_id: string;
	content: string;
	message_index: number;
	type: string;
	created_at: string;
	updated_at: string;
}
